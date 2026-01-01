import pickle
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import msvcrt
import os
import time

start_folder = os.getcwd()
print(f'Start folder {start_folder}')
filename = 'pickspeak.pk'
interval = 1800

# load your data back to memory when you need it
try:
    with open(filename, 'rb') as fil:
        seqcounter = pickle.load(fil)
        print(seqcounter)
except  FileNotFoundError:
    seqcounter = 1

destfolder = r"C:\Users\donal\Documents\wavtemp"

def listen(folder, album):
    global seqcounter, interval
    HOSTAPI_FILTER = 'DirectSound'  # The name of the host API (driver) to use
    NAME_FILTER = 'Line 1'  # The name of the microphone to use
    RATE = 44100  # Sample rate
    CHANNELS = 1  # Mono audio
    ext = '.wav'

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
    print('checking for input')
    gotsound = False
    for x in range(10):
        data: np.ndarray = sd.rec(int(2 * RATE), samplerate=RATE, channels=CHANNELS,
                              device=input_device["index"])
        sd.wait()
        print(f'max{np.ndarray.max(data):9.6f}')
        print(f'min{np.ndarray.min(data):9.6f}')
        print(np.ndarray.mean(data))
        if np.ndarray.max(data) > 0.1:
            gotsound = True
            break
    if not gotsound:
        print('no sound detected')
        return

    # data recorded as 'float32' by default with +1.0 and -1.0 as the maximum and minimum values, respectively
    data: np.ndarray = sd.rec(int(interval * RATE), samplerate=RATE, channels=CHANNELS, device=input_device["index"])

    destname = f'{album}_pt_{seqcounter}{ext}'
    dest = os.path.join(folder, destname)
    # Record the start time
    start_time = time.perf_counter()

    while True:
        # Check for key press
        time.sleep(2)
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8').lower()
            if key == 'q':
                print("\nStopping recording...")
                break

        # Record the end time
        end_time = time.perf_counter()
        elapsed_seconds = int(end_time - start_time)
        if elapsed_seconds % 100 < 3:
            print(f'Elapsed seconds: {elapsed_seconds}')

        if elapsed_seconds > interval:
            start_time = end_time
            sd.wait()
            write(dest, RATE, data)
            print(data)
            time.sleep(1)
            #hopefully resest the data
            data: np.ndarray = sd.rec(int(interval * RATE), samplerate=RATE, channels=CHANNELS,
                                      device=input_device["index"])
            seqcounter += 1
            destname = f'{album}_pt_{seqcounter}{ext}'
            print(f'Next file will be:{destname}')
            dest = os.path.join(destfolder, destname)
        time.sleep(2)

    # Wait for the recording to finish
    sd.wait()

    print(f'Saving file to:{dest}')
    write(dest, RATE, data)
    # set_tags(ext[1:], dest, artist, album)


if __name__ == "__main__":
    album = 'Just Tell Them'
    #newalbum = input('Change album currently' + album)
    #album = newalbum or album
    listen(destfolder, album)
    with open(filename, 'wb') as fil:
        print(filename)
        print(seqcounter)
        pickle.dump(seqcounter, fil)