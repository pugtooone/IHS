#! /bin/zsh -xv

# create a csv file with oldname as column A, newname as column B

# Removing the unicode zero-width space \u200b
# sed "s/$(echo -ne '\u200b')//g" *.csv
# sed 's/\r//g' removing ^M

# problem to be solved
# 1) % at the end of the last row of csv needs to be removed

if [[ -e $1 ]]; then
    cd $1	
    cat *.csv | sed 's/\r//g' | while IFS=, read -r oldname newname; do
        rename -s $oldname $newname **/*(.)
    done
else
    print "target directory missing!!!"
fi
