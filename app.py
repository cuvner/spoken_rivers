import json
import pyaudio
import numpy as np
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key="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")

# Open and read the JSON file
with open('processed_river_names.json', 'r') as file:
    data = json.load(file)

# Print got data
if data:
    print('Data loaded')


def play_sound(text: str, speed: float = 1.0) -> None:
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Get the index of the loopback device
    loopback_device_index = None
    for i in range(p.get_device_count()):
        dev_info = p.get_device_info_by_index(i)
        print(f"Device {i}: {dev_info['name']}")
        if "Multi-Output Device" in dev_info['name']:  # Adjust the name based on your loopback software
            loopback_device_index = i
            break

    if loopback_device_index is None:
        print("Loopback device not found")
        exit()

    # Set up the sound player to use the loopback device
    player = p.open(format=pyaudio.paInt16, 
                    channels=1, 
                    rate=int(24000 * speed), 
                    output=True, 
                    output_device_index=loopback_device_index)

    # Get the speech from OpenAI
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="alloy",
        response_format="pcm",
        input=text,
    ) as response:
        # Play the sound with speed control
        for chunk in response.iter_bytes(chunk_size=1024):
            audio_data = np.frombuffer(chunk, dtype=np.int16)
            player.write(audio_data.tobytes())

    # Clean up the audio player
    player.stop_stream()
    player.close()
    p.terminate()


# Main loop to iterate through data and play sounds
for x in data:
    play_sound(x, speed=1)
