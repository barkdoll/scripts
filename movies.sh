# Convert all movies in library using ffmpeg
for thing in *; do
  if [[ -d "$thing" ]]; then
    echo "$thing | directory";
  elif [[ -f "$thing" ]]; then
    echo "$thing | file";
  else
    echo "$thing | invalid";
  fi
done


# TODO: add lots of conditionals lol
# TODO: if [ -d "$thing" ]; then
#         if [ -f *.mkv ] in "$thing/*"; do
#           ~/scripts/ffmkv.sh
#         if [ -f *.mp4 ] in "$thing/*"; do
#           ~/scripts/ffmp4.sh