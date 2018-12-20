# alias for this script could be maybe?
# alias bt="~/scripts/bt_watch_win10.sh | tee ~/scripts/bt-$(date +"%Y%m%d-%Hh%Mm").log"

# Make sure this points to your torrent client's binary
BT_CLIENT="C:\Program Files\qBittorrent\qbittorrent.exe"

# Get initial IP
ip=$(ipconfig | grep 'TAP' -A 7 | grep 'IPv4' | awk '{print $14}')
echo "" # padding
echo "watching IP for OpenVPN virtual adapter (TAP)"
# Bash equivalent of a ternary
[ "$ip" == "" ] && echo "current: NONE" || echo "current: $ip"
echo "" # padding

timer=$SECONDS # magic $SECONDS variable built into bash

change_ctr=0 # counter for IP changes per hour
while [ $change_ctr -le 2 ]; do 

	# Timer for resetting the $change_ctr
	elapsed=$(($SECONDS - $timer))
	if [ $elapsed -ge 3600 ]; then
		change_ctr=0
		timer=$SECONDS
		printf "IP changes counter reset \t\t\t $(date +"%Y.%m.%d %H:%M:%S")\n"
	fi

	current=$(ipconfig | grep 'TAP' -A 7 | grep 'IPv4' | awk '{print $14}')

	if [ "$current" != "$ip" ]; then
		# Kill qBittorrent if process exists
		pid=$(tasklist | grep 'qbittorrent' | awk '{print $2}')
		# Double slashes for Windows bash; idk why?
		# //F :	causes force termination
		# I needed it to get this working
		[ $pid ] && taskkill //PID "$pid" //F || true

		printf "change detected \t\t\t\t $(date +"%Y.%m.%d %H:%M:%S")\n"
		echo "killing qBittorrent"
		if [ "$current" == "" ]; then 
			echo "assigning new address or disconnected..."
		fi
		
		while [ "$current" == "" ]; do
			current=$(ipconfig | grep 'TAP' -A 7 | grep 'IPv4' | awk '{print $14}')
			sleep 0.25
		done

		# Does not count blank IPs as a change
		if [ "$ip" != "" ]; then
			change_ctr=$((change_ctr+1))
			# Script escape
			if [ $change_ctr -gt 2 ]; then
				echo "hourly change limit reached ($change_ctr)"
				echo ""
				exit 0
			fi
		fi

		ip=$current
		printf "new address assigned: $ip \t\t $(date +"%Y.%m.%d %H:%M:%S")\n"

		echo "starting qBittorrent"
		"$BT_CLIENT" & # put it in the background

		printf "changed "$change_ctr"x in current interval (hourly) \t $(date +"%Y.%m.%d %H:%M:%S")\n"
	fi
	sleep 1
done