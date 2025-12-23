import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import msvcrt

HOSTAPI_FILTER = 'DirectSound'  # The name of the host API (driver) to use
#NAME_FILTER = 'UMM-6'  # The name of the microphone to use
NAME_FILTER = 'Line 1'  # The name of the microphone to use
RATE = 44100  # Sample rate
DURATION = 5  # Duration to record
CHANNELS = 1  # Mono audio

# Find the host API matching the required filter
matching_hostapis = [idx for idx, h in enumerate(sd.query_hostapis()) if HOSTAPI_FILTER in h['name']]
if not matching_hostapis:
    raise ValueError(f'Hostapi matching name filter ({NAME_FILTER}) not found.')

idx_h = matching_hostapis[0]

matching_devices = [device for device in sd.query_devices()
                    if device['max_input_channels'] > 0
                    and NAME_FILTER in device.get('name')
                    and device['hostapi'] == idx_h]

if not matching_devices:
    raise ValueError(f'Device matching name filter ({NAME_FILTER}) not found.')

input_device = matching_devices[0]
print(input_device)
# data recorded as 'float32' by default with +1.0 and -1.0 as the maximum and minimum values, respectively
data: np.ndarray = sd.rec(int(DURATION * RATE), samplerate=RATE, channels=CHANNELS, device=input_device["index"])

while True:
    # Check for key press
    if msvcrt.kbhit():
        key = msvcrt.getch().decode('utf-8').lower()
        if key == 'q':
            print("\nStopping recording...")
            break

# Wait for the recording to finish
sd.wait()

# Save as WAV file
write("output.wav", RATE, data)