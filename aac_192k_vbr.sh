#########################################
# Converts FLAC files to my preferred
# lossy quality/format specs:
# 	AAC (*.m4a) files @ 192kbps (VBR)
#
# Requirements:
#	- UNIX-like shell environment
#	- GNU find
#	- realpath
#	- ffmpeg
#########################################

aac_192k() {
	input="${1}"
	# removes trailing slashes from the target directory ($2) 
	# and renames the FLAC file with m4a
	output="$(echo "$2" | sed 's:/*$::')/$(basename "${1%%.flac}.m4a")"
	
	ffmpeg -y -i "$input" -ab 192k -map_metadata 0 "$output"

	# Test file paths with:
	# echo "$input"
	# echo "-> $output"
	# echo " "
}

# so that sub-shells can see it
export aac_192k


if [ -z "$1" -o -z "$2" -o -n "$3" ]; then
	echo "Exactly two arguments required:"
	echo "$(basename "$0") <input-path> <output-path>"
	exit 1
fi

source="$(realpath "$1")"
target="$(realpath "$2")"

# Create subfolder with the same name
# as the source directory (which should be the album folder)
working_dir="$source/$(basename "${source}")"
[ ! -d "$working_dir" ] && mkdir "$working_dir" && echo "created sub-directory '$working_dir'"

# echo "initializing encode job..."
# removed  -printf "%f\n"
find "$source" -maxdepth 1 -name "*.flac" | while read file; 
do
	aac_192k "$(realpath "$file")" "${working_dir}"
done

# Copy cover images
echo "searching for cover art..."
for image in "$source"/cover*; do
	case "$image" in 
	*.jpg | *.jpeg | *.png | *.tiff | *.gif)
		echo "$image"
		cp "$image" "${working_dir}/";
		;;
	*) # default fallback
	 	true
	 	;;
	esac
done

mv "$working_dir" "$target/"
echo "moved to '$target/$(basename "$working_dir")'"
echo "encoding job finished!"
exit 0
