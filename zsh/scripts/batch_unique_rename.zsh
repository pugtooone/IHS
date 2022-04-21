#! /bin/zsh -xv

# Removing the unicode zero-width space \u200b
# sed "s/$(echo -ne '\u200b')//g" *.csv

cat *.csv | while IFS=, read -r oldname newname; do

	rename -s $oldname $newname Images/*

done
