subfolder="${PWD##*/}"
if [ ! -d "$subfolder" ]; then
	mkdir $subfolder
fi

for gainz in *.{mp4,mkv} ; do 
	ffmpeg -i "$gainz" -q:a 3 -c:a libmp3lame "$subfolder/${gainz%.*}.mp3"
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
