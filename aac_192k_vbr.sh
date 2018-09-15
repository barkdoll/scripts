# Converts FLAC files to my preferred 
# lossy quality/format specs:
# AAC (*.m4a) files @ 192kbps (VBR)

# Requirements: 

  # qaac - https://sites.google.com/site/qaacpage/cabinet

  # libFLAC.dll - http://www.rarewares.org/lossless.php
  # OR go into the dependencies folder (same name as this script),
  # extract either 32/64-bit version depending on your OS,
  # rename libFLAC_dynamic.dll to libFLAC.dll,
  # and add it to any directory in your $PATH


# Create subfolder
subfolder="${PWD##*/}"
if [ ! -d "$subfolder" ]; then
	mkdir "$subfolder"
  echo "created sub-directory $subfolder";
fi

# Rename to qaac (remove 64) 
# if using 32-bit version
echo "initializing encode job...";
qaac64 *.flac -a192 -d "$subfolder";

printf "\n\n"

# Copy cover images
for image in cover*.jpg; do
  echo "searching for cover art...";
  cp "$image" "$subfolder/";
done

# Move subfolder to lossy audio directory
target=$(cd .. && echo `pwd`);
target="${target##*/}";

# target directory
t_dir="/m/audio_lossy/$target";

if [ ! -d "$t_dir" ]; then
  echo "target directory not found";
  echo "creating target directory...";
  mkdir "$t_dir";
  echo "created target directory $t_dir";
else
  echo "found target directory $t_dir";
fi


mv "$subfolder" "$t_dir/";
echo "moved $subfolder to $t_dir/$subfolder";

echo "encoding job finished!"
printf "\n\n";
exit 0