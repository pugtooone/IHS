#! /bin/zsh

# script for Kipling batch to vendor
# created by Zeric Chan

# Problem to be solved

exec > /tmp/kipling.log 2>&1 #log file

emulate -LR zsh
setopt extended_glob
setopt null_glob
setopt xtrace

local PS4=$'+%1N:[%i]:%_> '
print "executed at $(date "+%Y%m%d %H:%M")"

while [[ ! -d /Volumes/Studio ]]; do
  osascript -e "Server is not connected\nPlease reconnect before proceed"
done

while true; do

	# applescript for dialog box for choosing folder
	local target_folder_apple=$(osascript -e 'set theDocument to choose folder with prompt "Select the Kipling batch to process:"')
	local target_folder=$(print $target_folder_apple | sed -e 's/alias //' -e 's/Macintosh HD//' -e 's/:/\//g')

	# test if the target_folder is a valid Kipling batch
	if [[ ${(L)target_folder:t} == kipling* ]]; then

    		cd $target_folder
    		local PARENT="$(print $target_folder)"
        local SWATCH_BASE="/Volumes/Studio/CLIENTS/Kipling/Post-production/Kipling Color Swatch"

    		if [[ ! -d Images ]]; then
        		mkdir Images
    		fi
    		
    		# array for Kipling grid size
    		typeset -a GRID=( A1 A2 A3 A4 A5 B1 B2 B3 B4 B5 B6 TBC )
        local NUM_GRID=((${#GRID[@]} + 1))
    		
    		# move all product folders to the designated master grid size folders
    		for (( i=1 ; i<$NUM_GRID ; i++ )); do
	    		for dir in **/"${GRID[i]}"; do
		    		mkdir Images/"${GRID[i]}"
		    		local MGRID="${PARENT}/Images/${GRID[i]}"
		    		for dir in [^I]*/**/${GRID[i]}; do
			    		command ls -1 $dir | while read; do
                if [[ -e $SWATCH_BASE/${REPLY: -3}.* ]]; then
                  cp $SWATCH_BASE/${REPLY: -3}.(jpg|tif) ${dir}/${REPLY}/
                else
                  # convert the mainshot as jpeg and back up to the server
                  sips -s format jpeg ${dir}/${REPLY}/${REPLY}_(1|DSO).tif --out ${dir}/${REPLY}/${REPLY: -3}.jpg
                  if [[ -e ${dir}/${REPLY}/${REPLY}_DSO.tif ]]; then
                    mv ${dir}/${REPLY}/${REPLY: -3}.jpg ${SWATCH_BASE}/DSO/
                  else
                    mv ${dir}/${REPLY}/${REPLY: -3}.jpg ${SWATCH_BASE}/Regular/
                  fi
                fi
              done #end while loop
			    		cd $dir
			    		mv -n KPK* $MGRID
			    		cd $PARENT
		    		done
	    		done
    		done #end i loop
		break
	elif [[ ${target_folder_apple} == '' ]]; then
		exit 2
	else
		osascript -e 'display alert "Please select a Kipling batch!"'
		continue
	fi
done	
