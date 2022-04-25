#! /bin/zsh -xv

# Removing the unicode zero-width space \u200b
# sed "s/$(echo -ne '\u200b')//g" *.csv

# create a csv file with oldname as column A, newname as column B

cat *.csv | while IFS=, read -r oldname newname; do

		rename -s $oldname $newname Images/*

	    done
