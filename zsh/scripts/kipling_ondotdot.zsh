#! /bin/zsh

exec > /tmp/kipling_ondotdot.log 2>&1

emulate -LR zsh
setopt extended_glob
setopt null_glob
setopt xtrace

local PS4=$'+%1N:[%i]:%_> '
print "executed at $(date "+%Y%m%d %H:%M")"

#==================================================
#{{{ Folder Selections & JOB_PATH Construct
#==================================================

function display_javascript_alert() {
  osascript -l JavaScript <<-HERE
    
    const app = Application.currentApplication();
    app.includeStandardAdditions = true;

    app.displayAlert("${1}");
HERE
}

while true; do
  # native MacOS GUI prompt user for folder selection
  RESULT=( $(print $(osascript -l JavaScript <<-HERE

    const app = Application.currentApplication();
    app.includeStandardAdditions = true;
    
    function getFolder (){

      const outputFolder = app.chooseFolder({
        withPrompt: "Please select the kipling folder",
        multipleSelectionsAllowed: true
      });

      return outputFolder;
    };
    
    getFolder();

HERE
  ) | sed -e 's/ /;/g' -e 's/Path(//' -e 's/),;Path(/ /g' -e 's/)//' -e 's/"//g') ) # replace space with ; which will be substitued back later

  #continute to prompt for folder if none has been chosen
  if [[ $RESULT == "" ]]; then
    print "No folder has been chosen"
    typeset RESPONSE=$(osascript -l JavaScript <<-HERE
      
      const app = Application.currentApplication();
      app.includeStandardAdditions = true;

      app.displayAlert("No folder has been chosen", {
        buttons: ["Choose Again", "Cancel"],
      });
HERE
    )
    if [[ $RESPONSE == "buttonReturned:Cancel" ]]; then
      return 1
    fi
    continue
  fi

  typeset NUM_WRONG_FOLDER=0
  for dir in ${RESULT}; do
    if [[ ${dir} == /Volumes/Studio/* ]]; then
        display_javascript_alert "One of the selected folders is from server!\n\nPlease make sure the script is not used on server!"
        exit 1
    elif [[ "$(basename ${(L)dir})" != *kipling* ]]; then
      print "Non-Kipling folder: $(basename ${(L)dir})"
      $NUM_WRONG_FOLDER++
    fi
  done

  if [[ $NUM_WRONG_FOLDER == 0 ]]; then
    break
  else
    display_javascript_alert "None Kipling folder detected\nPlease double check"
  fi

done #end of while loop

# construct $JOB_NAME by appending all batch no.
local JOB_NAME="Kipling"

for dir in ${RESULT}; do
  dir=$(print ${dir//;/ })
  local JOB_NAME="${JOB_NAME} $(basename ${dir//Kipling /})"
done

# create $JOB_PATH as the master directory to store all the images to-be-uploaded
local JOB_PATH=$(dirname ${RESULT[1]} | sed 's/;/ /g')/$JOB_NAME
mkdir $JOB_PATH

for dir in ${RESULT}; do
  dir=$(print ${dir//;/ })

  #!!!ADD CONDITIONS FOR VARIOUS JOB TYPES
  mv -i ${dir}/**/*.(jpg|jpeg|png|tif|tiff) ${JOB_PATH}
  # rm the original dir if more than 1 is selected; rm the subfolder inside if only 1 is selected
  if [[ ${#RESULT} > 1 ]]; then
    rm -r ${dir}
  elif [[ ${#RESULT} == 1 ]]; then
    rm -r ${dir}/*(/)
  fi
done

print -l ${JOB_PATH}/*.(jpg|jpeg|png|tif|tiff) | while read; do
	basename ${REPLY}
done | pbcopy

osascript -l JavaScript <<-HERE
  const app = Application.currentApplication();
  app.includeStandardAdditions = true;

  app.displayAlert("Images info is copied to your clipboard", {
      buttons: ["Continue"]
  });
HERE

#==================================================
#}}}
#==================================================

#==================================================
#{{{ Prompts for Copying Info on Teams
#==================================================

open -a "Microsoft Teams"

# prompt user for copying the info on Teams
osascript -l JavaScript <<-HERE
  const app = Application.currentApplication();
  app.includeStandardAdditions = true;

  const alertMsg = "Step 1: Paste the copied info onto Teams\n\nStep 2: Copy the csv info\n(from B2 to AC)"
  app.displayAlert("Teams Information is needed\nPlease follow the following steps:", {
    message: alertMsg,
    buttons: ["Information Copied!"]
  });
HERE

# check if the content on clipboard is the correct format
while [[ "$(pbpaste | head -c 8)" != "filename" ]]; do
  osascript -l JavaScript <<-HERE

    const app = Application.currentApplication();
    app.includeStandardAdditions = true;

    app.displayAlert("Incorrect information", {
      message: "Please make sure you copy the correct info.",
      buttons: ["Information Copied!", "Cancel"],
    });
HERE
  if [[ $RESPONSE == "buttonReturned:Cancel" ]]; then
    return 1
  fi
done
#==================================================
#}}}
#==================================================

#==================================================
#{{{ CSV Construct
#==================================================
# constructing csv
local TMP_CSV="/tmp/kipling_csv_tmp.csv"
local CSV_TO_CLIENT="${JOB_PATH}/../$(date "+%Y%m%d")_${JOB_NAME}.csv"
local CSV_TO_THE_DOT="${JOB_PATH}/../${JOB_NAME}.csv"

echo -ne '\xEF\xBB\xBF' > ${CSV_TO_THE_DOT}

pbpaste | sed 's/,/;/g' | sed 's/\t/,/g' > ${CSV_TO_CLIENT}
pbpaste | sed 's/\t/;/g' > ${TMP_CSV}

iconv -f CP1252 -t UTF-8 ${TMP_CSV} >> ${CSV_TO_THE_DOT}
#==================================================
#}}}
#==================================================

display_javascript_alert "Batch is ready to upload!";

open ${JOB_PATH}
