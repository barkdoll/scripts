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

# Looks for jpg cover image
if [ -f "cover.jpg" ]; then
	cp "cover.jpg" "$subfolder/"
	printf "cover.jpg copied successfully...\n"
else
	printf "no cover.jpg found...\n"
fi

# Looks for png cover image
if [ -f "cover.png" ]; then
	cp "cover.png" "$subfolder/"
	printf "cover.png copied successfully...\n"
else
	printf "no cover.png found...\n"
fi

mv "$subfolder" "/m/audio_immersion/$subfolder"

printf "Done moving files. Go check on your stuff!\n\n"
