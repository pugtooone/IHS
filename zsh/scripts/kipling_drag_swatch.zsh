#! /bin/zsh

exec > /tmp/kipling_drag_swatch.log 2>&1

emulate -LR zsh
setopt extended_glob
setopt null_glob
setopt xtrace

local PS4=$'+%1N:[%i]:%_> '
print "executed at $(date "+%Y%m%d %H:%M")"

#==================================================
#{{{
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
    display_javascript_alert "No folder has been chosen"
    print "No folder has been chosen"
    continue
  fi

  local NUM_WRONG_FOLDER=0
  for dir in ${RESULT}; do
    if [[ "$(basename ${(L)dir})" != *kipling* ]]; then
      print "Non-Kipling folder: $(basename ${(L)dir})"
      ${NUM_WRONG_FOLDER}++
    fi
  done

  if [[ $NUM_WRONG_FOLDER == 0 ]]; then
    break
  else
    display_javascript_alert "None Kipling folder detected\nPlease double check"
  fi

done #end of while loop

#alert user if server is not connected
while true; do
  if [[ -d /Volumes/Studio ]]; then
    local SWATCH_BASE="/Volumes/Studio/CLIENTS/Kipling/Post-production/Kipling Color Swatch"
    break
  else
    display_javascript_alert "Server is not connected\nPlease connect before proceed"
  fi
done

for job_dir in ${RESULT}; do
  local job_dir=$(print ${dir//;/ })
  #local NUM_PROD_DIR="$(print -l ${job_dir}/**/(TIF|TIFF|tif|tiff)/KPK*(/) | wc -l)"
  #local NUM_PROD_DIR_DONE=0
  for dir in ${job_dir}/**/(TIF|TIFF|tif|tiff)/KPK*(/); do
    #${NUM_PROD_DIR_DONE}++
    #display_javascript_alert "Copying Swatches:\n${NUM_PROD_DIR_DONE}/${NUM_PROD_DIR}"
    cp -f "${SWATCH_BASE}"/**/${dir: -3}.* $dir
    cp -f "${SWATCH_BASE}"/**/"Monkey Skin Colour.jpg" $dir
  done
done

display_javascript_alert "Swatches are copied"

#==================================================
#}}}
#==================================================
