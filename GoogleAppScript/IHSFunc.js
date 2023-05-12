/*

Check Amendment Trackers by clicking a custom menu item to run script

OAuth scope set up:
1. Google Sheet > Extensions > Apps Script > Project Settings
2. Turn on 'Show "appsscript.json" manifest file in editor'
3. Edit appsscript.json {..."oauthScopes": ["https://www.googleapis.com/auth/spreadsheets"]...}

*/

/** @OnlyCurrentDoc */

//Custom menu on tool bar
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('IHS Functions')
      .addItem('Check Amendment', 'checkAmendment')
      .addToUi();
}

function checkAmendment() {

  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Outstanding Amendment');

  //reset the background colour
  sheet.getRange('B4:D10').setBackground('#f3f3f3');

  //rm URL for privacy
  const brandTrackers = {
    'Agnes b': 'https://...',
    'AIWA': 'https://...',
    'Arena': 'https://...',
    'Esprit': 'https://...',
    'Fred Perry': 'https://...',
    'New Balance': 'https://...',
    'OnTheList': 'https://...',
    'Petit Bateau': 'https://...',
    'Satami': 'https://...',
    'Toy R US': 'https://...',
    'WEAT': 'https://...'
  };

  let amendmentInfo = [];
  let msg = "There are outstanding amendments for:\n\n";

  for (let brand in brandTrackers) {
    const url = brandTrackers[brand];
    const statusCol = SpreadsheetApp.openByUrl(url).getRangeByName('amendment_status');
    const statusVal = statusCol.getValues();
    let amendmentNum = 0;

    for (const status of statusVal) {
      if (status == 'INCOMPLETE') {
        amendmentNum += 1;
      };
    };

    if (amendmentNum > 0) {
      msg += "- " + brand + "\n";
      let newInfo = [[brand], [amendmentNum], [url]];
      amendmentInfo.push(newInfo);
    };

  };

  const numRow = 3 + amendmentInfo.length;
  const range = sheet.getRange('B4:D' + numRow.toString());

  //formatting background color
  sheet.getRange('B4:B' + numRow.toString()).setBackground('#1c7685');
  sheet.getRange('C4:D' + numRow.toString()).setBackground('#c1dfe5');

  //update the Outstanding Amendments sheet
  range.setValues(amendmentInfo);

  //GUI alert to display brands with outstanding amendments
  SpreadsheetApp.getUi().alert(msg);

}
