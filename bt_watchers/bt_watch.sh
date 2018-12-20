# alias for this script could be maybe?
# alias bt="~/scripts/bt_watch.sh | tee ~/scripts/bt-$(date +"%Y%m%d-%Hh%Mm").log"

# Get initial IP
ip=$(ifconfig | grep 'tun0' -A 7 | grep 'inet addr' | sed 's/.*inet addr:\([0-9\.]*\).*/\1/')
echo "" # padding
echo "watching IP for OpenVPN virtual adapter (tun0)"
# Bash equivalent of a ternary
[ "$ip" == "" ] && echo "current: NONE" || echo "current: $ip"
# Start qBittorrent if tun0 address found (which means VPN is running)
[ "$ip" ] && (qbittorrent&) || echo "client not started; no tun0 address found"
echo "" # padding


timer=$SECONDS # magic $SECONDS variable built into bash
change_ctr=0 # counter for IP changes per hour
while [ $change_ctr -le 2 ]; do 

	# Timer for resetting the $change_ctr
	elapsed=$(($SECONDS - $timer))
	if [ $elapsed -ge 3600 ]; then
		timer=$SECONDS
		# Only reset counter if not 0
		if [ "$change_ctr" -ne 0 ]; then
			change_ctr=0
			printf "$(date +"%Y.%m.%d %H:%M:%S")\t IP change counter reset\n"
		else
			printf "$(date +"%Y.%m.%d %H:%M:%S")\t No IP changes in the last hour\n"
		fi
	fi

	current=$(ifconfig | grep 'tun0' -A 7 | grep 'inet addr' | sed 's/.*inet addr:\([0-9\.]*\).*/\1/')

	if [ "$current" != "$ip" ]; then
		# Kill qBittorrent if process exists
		[ $(pgrep 'qbittorrent') ] && killall -v 'qbittorrent' || true

		printf "$(date +"%Y.%m.%d %H:%M:%S")\t change detected\n"
		echo "killing qBittorrent"
		if [ "$current" == "" ]; then 
			echo "assigning new address or disconnected..."
		fi
		
		while [ "$current" == "" ]; do
			current=$(ifconfig | grep 'tun0' -A 7 | grep 'inet addr' | sed 's/.*inet addr:\([0-9\.]*\).*/\1/')
			sleep 0.25
		done

		# Does not count blank IPs as a change
		if [ "$ip" != "" ]; then
			change_ctr=$((change_ctr+1))
			# Script escape
			if [ $change_ctr -gt 2 ]; then
				printf "$(date +"%Y.%m.%d %H:%M:%S")\t hourly change limit reached ($change_ctr)\n"
				exit 0
			fi
		fi

		ip=$current
		printf "$(date +"%Y.%m.%d %H:%M:%S")\t new address assigned: $ip"

		echo "starting qBittorrent"
		qbittorrent& # start client in the background

		printf "$(date +"%Y.%m.%d %H:%M:%S")\t changed "$change_ctr"x in current interval (hourly)\n"
	fi
	sleep 1
done