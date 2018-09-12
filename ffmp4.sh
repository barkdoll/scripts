# NOTE: you can find the track ID of the audio stream 
# you want to pass in your $1 argument by using:
# mkvmerge -i <filename>

subfolder="${PWD##*/}"
if [ ! -d "$subfolder" ]; then
	mkdir "$subfolder"
fi


# Derived from 
# https://unix.stackexchange.com/questions/9496/looping-through-files-with-spaces-in-the-names
find . -type f \( -name "*.mp4" -or -name "*.avi" \) -exec bash -c '
	for file in "$0"; do 
		basename="${file##*/}"
		basename="${basename%.*}.mp3"
		ffmpeg -i "$file" -q:a 3 -c:a libmp3lame "$1/$basename"
	done
	' {} "$subfolder" \;


printf "\n\n----- Done converting audio -----\n\n"

# Copy cover images
for c in cover*.{jpg,png}; do
	cp "$c" "$subfolder/"
	printf "$c copied successfully...\n"
done

mv "$subfolder" "/m/audio_immersion/$subfolder"

printf "Done moving files. Go check on your stuff!\n\n"
