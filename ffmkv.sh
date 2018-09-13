# NOTE: you can find the track ID of the audio stream 
# you want to pass in your $1 argument by using:
# mkvmerge -i <filename>

# Checks for a stream selection argument. If no argument is given, 
# the script uses the first audio track (stream #0) by default.
if [[ "$1" ]]; then
	mks="$1"
else
	mks="1"
fi

# Variable expansion to make subfolder name same as parent
subfolder="${PWD##*/}"
if [ ! -d "$subfolder" ]; then
	mkdir "$subfolder"
fi


# Derived from 
# https://unix.stackexchange.com/questions/9496/looping-through-files-with-spaces-in-the-names
find . -type f -name "*.mkv" -exec bash -c '
	for file in "$0"; do 
		basename="${file##*/}"
		basename="${basename%.*}.mp3"
		ffmpeg -i "$file" -map 0:"$1" -q:a 3 -c:a libmp3lame "$2/$basename"
	done
	' {} "$mks" "$subfolder" \;

printf "\n\n----- Done converting audio -----\n\n"

# Copy cover images
for c in cover*.{jpg,png}; do
	cp "$c" "$subfolder/"
	printf "$c copied successfully...\n"
done

mv "$subfolder" "/m/audio_immersion/$subfolder"

printf "Done moving files. Go check on your stuff!\n\n"
