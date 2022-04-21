#! /bin/zsh -xv

# script for Kipling batch to vendor
# created by Zeric Chan

cd kipling_test
local PARENT="$(pwd)"
mkdir Images
local Img="$(pwd)"/Images
touch swatch.txt
local SWATCH="swatch.txt"

# array for Kipling grid size

KIPGRID=( A1 A2 A3 A4 A5 B1 B2 B3 B4 B5 B6 TBC )

# move all product folders to the designated master grid size folders

for (( i=1 ; i<13 ; i++ )); do

	for dir in **/*"${KIPGRID[i]}"; do

		mkdir Images/"${KIPGRID[i]}"
		local MGRID="${Img}/${KIPGRID[i]}"

		for dir in [^I]*/**/*${KIPGRID[i]}; do
                	
			ls -1 $dir | while read; do
			print "OR name: $(cut -c $(( ${#REPLY} - 2 ))-)" >> $SWATCH
			done
			
			cd $dir
			mv -i * $MGRID
			cd $PARENT
		done
	done
done
