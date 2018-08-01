# This script requires a folder named 'fukuonsei' because I use it 
# to merge extra audio streams to video files
# 'fukuonsei' means 'second (supplementary) sound channel​' in Japanese

# check for fukuonsei directory to make sure we can mux the files
if [ ! -d "fukuonsei" ]; then
    printf "\nWhoops! I can't find your 'fukuonsei' directory.\n\n"
    exit 0
fi

if [ ! -d "muxed" ]; then
	mkdir "muxed"
fi


for v in *.mp4; do
	prefix="${v%.*}"
	output="$prefix.mkv"
	mkvmerge --title "$prefix" --track-order "0:0,0:1,1:1" --default-language "jpn" -o "muxed/$output" --track-name "1:日本語" --language "1:jpn" "${v}" -D --track-name "1:日本語 - 副音声" --language "1:jpn" "fukuonsei/${v}"
done

printf "\n\n\n----- Multiplexing completed -----\n\n\n\n"
exit 0
