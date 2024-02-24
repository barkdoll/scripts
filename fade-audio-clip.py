import os
import ffmpeg
from argparse import ArgumentParser
from pathlib import Path
from datetime import datetime

def main(input_file: Path, *, fade_in_duration=0.3, fade_out_duration=0.3, target_volume_db=-3.0):
    if not os.path.isfile(input_file):
        raise Exception("Provided audio file is not valid or does not exist.")

    probe = ffmpeg.probe(input_file)

    audio_duration = float(probe['streams'][0]['duration'])
    
    now = datetime.now()
    output_file_name = now.strftime("%Y%m%d-%H%M%S") 

    # Apply fade-in at the start and fade-out at the end
    output_directory = input_file.parent.absolute()
    audio = (
        ffmpeg
            .input(input_file)
            .filter('loudnorm', i='-24', lra='7', tp='-2')
            .filter('afade', type='in', start_time=0, duration=fade_in_duration)
            .filter('afade', type='out', start_time=(audio_duration - fade_out_duration), duration=fade_out_duration)
            .output(str(Path(output_directory, f'{output_file_name}.mp3')))
    )

    # Execute FFmpeg command
    audio.run()

if __name__ == "__main__":
    parser = ArgumentParser(description="Normalize, fade-in, and fade-out and audio clip and output to the same location with a timestamp filename (e.g. 20231105-121836.mp3)")
    parser.add_argument("path")
    parser.add_argument("-fi", "--fade-in", default=0.3)
    parser.add_argument("-fo", "--fade-out", default=0.3)
    parser.add_argument("-vol", "--max-volume-db", default=-3.0)
    args = parser.parse_args()
    main(
        Path(args.path), 
        fade_in_duration=args.fade_in, 
        fade_out_duration=args.fade_out,
        target_volume_db=args.max_volume_db
    )
