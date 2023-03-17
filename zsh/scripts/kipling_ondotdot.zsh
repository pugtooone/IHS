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

# quit function if no folder has been chosen
if [[ $RESULT == "" ]]; then
  osascript -l JavaScript <<-HERE
    
    const app = Application.currentApplication();
    app.includeStandardAdditions = true;

    app.displayAlert("No folder has been chosen");

HERE
  print "No folder has been chosen"
  return 2
fi

# construct $JOB_NAME by appending all batch no.
local JOB_NAME="Kipling"

for dir in ${RESULT}; do
  dir=$(print ${dir//;/ })
  local JOB_NAME="${JOB_NAME} $(basename ${dir//Kipling /})"
  if [[ "$(basename ${(L)dir})" != kipling* ]]; then
    osascript -l JavaScript <<-HERE
      const app = Application.currentApplication();
      app.includeStandardAdditions = true;

      app.displayAlert("Some of the selections are not Kipling batch")
HERE
    return 2
  fi
done

# create $JOB_PATH as the master directory to store all the images to-be-uploaded
local JOB_PATH=$(dirname ${RESULT[1]} | sed 's/;/ /g')/$JOB_NAME
mkdir $JOB_PATH

for dir in ${RESULT}; do
  dir=$(print ${dir//;/ })
  mv -i ${dir}/**/*.(jpeg|jpg|png) ${JOB_PATH}
  rm -r ${dir}
done

#==================================================
#}}}
#==================================================

#==================================================
#{{{ Archived Codes
#==================================================
## prompt user to input job name
#JOB_NAME=$(osascript -l JavaScript <<-HERE

  #function promptForJob(){

    #const app = Application.currentApplication();
    #app.includeStandardAdditions = true;

    #const response = app.displayDialog("What's Batch Name?", {
        #defaultAnswer: "",
        #withIcon: "note",
        #buttons: ["Cancel", "Continue"],
        #defaultButton: "Continue"
    #});

    #if (response.textReturned == ""){
      #return "";
    #};

    #app.displayAlert("Please Copy the information on the TEAMS template now", {
      #buttons: ["Information Copied!"]
    #});

    #return response.textReturned;
  #};

  #promptForJob();

#HERE
#)

## quit if "Cancel" was pushed in the app.displayDialog
#if [[ ${JOB_NAME} == "" ]]; then
  #osascript -l JavaScript <<-HERE

    #const app = Application.currentApplication();
    #app.includeStandardAdditions = true;

    #app.displayAlert("No batch name has been input")

#HERE
  #return 2
#fi

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

  app.displayAlert("Please Copy the information on the TEAMS template now", {
    buttons: ["Information Copied!"]
  });
HERE

# check if the content on clipboard is the correct format
if [[ "$(pbpaste | head -c 8)" != "filename" ]]; then
  osascript -l JavaScript <<-HERE

    const app = Application.currentApplication();
    app.includeStandardAdditions = true;

    app.displayAlert("Incorrect information", {
      message: "Please make sure you copy the correct info."
    });
HERE
  return 2
fi
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
