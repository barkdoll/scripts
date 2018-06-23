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
	output="${v%.*}.mkv"
	prefix="${v%.*}"
	mkvmerge --title "$prefix" --track-order "0:1,0:0,1:0" --default-language "jpn" -o "muxed/$output" --track-name "0:日本語" --language "0:jpn" --default-track "0" "${v}" -D --track-name "0:日本語 - 副音声" --language "0:jpn" "fukuonsei/${v}"
done

printf "\n\n\n----- Multiplexing completed -----\n\n\n\n"
exit 0
