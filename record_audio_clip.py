import wave
from os.path import expanduser
from pathlib import Path
from pyaudio import PyAudio, paInt16
from fade_audio_clip import process_audio_file

def record_until_user_exit():
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = 3
    filename = "output.wav"

    audio = PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = audio.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    try:
        while True:
            data = stream.read(1024)
            frames.append(data)
    except KeyboardInterrupt:
        pass

    stream.stop_stream()
    stream.close()
    audio.terminate()

    home_dir = expanduser("~")
    desktop_temp_file_path = Path(home_dir, "Desktop", "tmp.wav")
    sound_file = wave.open(str(desktop_temp_file_path), "wb")
    sound_file.setnchannels(channels)
    sound_file.setsampwidth(audio.get_sample_size(paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()

    return desktop_temp_file_path
    

def main():
    tmp_file = record_until_user_exit()
    process_audio_file(tmp_file)


if __name__ == '__main__':
    main()
