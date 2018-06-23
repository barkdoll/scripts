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

subfolder="${PWD##*/}"
if [ ! -d "$subfolder" ]; then
	mkdir $subfolder
fi

for gainz in *.mkv ; do 
	ffmpeg -i "$gainz" -map 0:"$mks" -q:a 3 -c:a libmp3lame "$subfolder/${gainz%.*}.mp3"
done

printf "\n\n\n\nDone converting audio...\n\n\n\n"

# Looks for jpg cover image
if [ -f "cover.jpg" ]; then
	cp "cover.jpg" "$subfolder/"
	printf "\n\ncover.jpg copied successfully...\n\n"
else
	printf "\n\nno cover.jpg found...\n\n"
fi

# Looks for png cover image
if [ -f "cover.png" ]; then
	cp "cover.png" "$subfolder/"
	printf "\n\ncover.png copied successfully...\n\n"
else
	printf "\n\nno cover.png found...\n\n"
fi

# move the new folder of audio files to where?
mv "$subfolder" "insert-new-folder-destination-here"

printf "\n\nDone moving files. Go check on your stuff!\n\n\n\n\n"
