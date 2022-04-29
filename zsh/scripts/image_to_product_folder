#! /bin/zsh -xv

# This script should be put in the directory containing the images, in which the images are all inside the parent directory
# make directory with the sku (cut command should be customised according to the requirement)
ls -1 | cut -d. -f1 | while read; do

  mkdir $REPLY

done

# drag image to designated directory
print -l *(/) | while read; do

  mv -i ${REPLY}.* ${REPLY}

done
