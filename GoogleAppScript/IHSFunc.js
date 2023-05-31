/*

Check Amendment Trackers by clicking a custom menu item to run script

OAuth scope set up:
1. Google Sheet > Extensions > Apps Script > Project Settings
2. Turn on 'Show "appsscript.json" manifest file in editor'
3. Edit appsscript.json {..."oauthScopes": ["https://www.googleapis.com/auth/spreadsheets"]...}

*/

/** @OnlyCurrentDoc */

function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('IHS Functions')
    .addItem('Check Amendment', 'checkAmendment')
    .addItem('Integrate Shotlists', 'integrateShotlistsUI')
    .addToUi();
};

function createTimeTrigger() {
  //time-trigger to run everyday between 0800-0900
  ScriptApp.newTrigger('integrateShotlists')
                      .timeBased()
                      .atHour(8)
                      .everyDays(1)
                      .inTimezone("Asia/Hong_Kong")
                      .create();
  
  ScriptApp.newTrigger('checkAmendment')
                      .timeBased()
                      .atHour(8)
                      .everyDays(1)
                      .inTimezone("Asia/Hong_Kong")
                      .create();
};

function integrateShotlistsUI() {
  integrateShotlists();
};

function integrateShotlists() {

  SpreadsheetApp.flush();

  const sourceSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Brand Status');

  //get the coordinates for headeer "Brand"
  let txtFinder = sourceSheet.createTextFinder('Brand');
  let brandRange = txtFinder.findNext();
  const brandRow = brandRange.getRow();
  const brandCol = brandRange.getColumn();

  //change the 4th arugment if new header is added
  const sourceHeader = sourceSheet.getRange(brandRow, brandCol, 1, 19).getValues();
  const sourceHeaderObj = {};
  for (let i = 0; i < sourceHeader[0].length; i++) {
    const header = sourceHeader[0][i];
    const col = brandCol + i;
    sourceHeaderObj[header] = col;
  };

  const prettySourceHeaderObj =JSON.stringify(sourceHeaderObj, null, 2);
  Logger.log(prettySourceHeaderObj);

  const brandObj = {};

  const sourceActiveBrandList = sourceSheet.createTextFinder('Active').matchEntireCell(true).findAll(); //getting the range of all 'Active' cells
  
  //defining global variable for kipling to remove it from the active brand list later
  let kiplingCell;

  for (let i = 0; i < sourceActiveBrandList.length; i++) {
    const row = sourceActiveBrandList[i].getRow();
    const activeBrand = sourceSheet.getRange(row, sourceHeaderObj.Brand).getValue();
    Logger.log('Active Brand: ' + activeBrand);
    //ignore Kipling
    if (activeBrand == "Kipling") {
      kiplingCell = sourceSheet.getRange(row, sourceHeaderObj.Brand);
      continue;
    };

    //construct individual active brand data
    const activeBrandData = {};
    for (let i = 0; i < sourceHeader[0].length; i++) {
      const key = Object.keys(sourceHeaderObj)[i];
      const val = sourceSheet.getRange(row, Object.values(sourceHeaderObj)[i]).getValue();
      activeBrandData[key] = val;
      delete activeBrandData.Brand;
    };

    brandObj[activeBrand] = activeBrandData;
  };

  sourceActiveBrandList.pop(kiplingCell);
  
  Logger.log('No. of Active Brands: ' + sourceActiveBrandList.length);
  Logger.log('brand obj: ' + Object.keys(brandObj).length);
  const prettyBrandObj = JSON.stringify(brandObj, null, 2);
  Logger.log(prettyBrandObj);

  //construct brand report

  const brandReports = {};
  const brandReportsData = []; //to write on the actual sheet

  for (let brand in brandObj) {
    const url = brandObj[brand]["Shotlist link"];
    const sheetName = brandObj[brand]["Sheet Name"];
    const prodWord = brandObj[brand]["SKU Name"];
    const shootNoteWord = brandObj[brand]["Shoot Note"];
    const dnsWord = brandObj[brand]["DNS Word"];
    const flatlayWord = brandObj[brand]["Flatlay Word"];
    const tabletopWord = brandObj[brand]["Tabletop Word"];
    const mannequinWord = brandObj[brand]["Mannequin Word"];
    const modelShootNoteWord = brandObj[brand]["Model Only Word"];
    const creativeShootNoteWord = brandObj[brand]["Creative Word"];
    const recDateWord = brandObj[brand]["Receive Date Word"];
    const ecomShotDateWord = brandObj[brand]["Ecom Shot Date Word"];
    const ecomImgNumWord = brandObj[brand]["No. of Ecom Img Word"];
    const modelShotDateWord = brandObj[brand]["Model Shot Date Word"];
    const modelImgNumWord = brandObj[brand]["No. of Model Img Word"];
    const creativeShotDateWord = brandObj[brand]["Creative Shot Date Word"];
    const creativeImgNumWord = brandObj[brand]["No. of Creative Img Word"];

    const brandShotlist = SpreadsheetApp.openByUrl(url).getSheetByName(sheetName);
    Logger.log('Accessing ' + brand + ' Shotlist');
    const brandShotlistData = brandShotlist.getDataRange().getValues();
    const lastRow = brandShotlist.getLastRow();
    const headerRow = brandShotlist.createTextFinder(recDateWord).matchEntireCell(true).findNext().getRow() - 1;
    const prodCol = brandShotlist.createTextFinder(prodWord).matchEntireCell(true).findNext().getColumn() - 1;
    const shootNoteCol = brandShotlist.createTextFinder(shootNoteWord).matchEntireCell(true).findNext().getColumn() - 1;
    const recDateCol = brandShotlist.createTextFinder(recDateWord).matchEntireCell(true).findNext().getColumn() - 1;
    const ecomShotDateCol = brandShotlist.createTextFinder(ecomShotDateWord).matchEntireCell(true).findNext().getColumn() - 1;
    const ecomShotCountCol = brandShotlist.createTextFinder(ecomImgNumWord).matchEntireCell(true).findNext().getColumn() - 1;
    //only init model if there are corresponding headers
    let modelShotDateCol = 0;
    let modelShotCountCol = 0;
    if (modelShotDateWord != "" & modelImgNumWord != "") {
      modelShotDateCol = brandShotlist.createTextFinder(modelShotDateWord).matchEntireCell(true).findNext().getColumn() - 1;
      modelShotCountCol = brandShotlist.createTextFinder(modelImgNumWord).matchEntireCell(true).findNext().getColumn() - 1;
    };
    let creativeShotDateCol = 0;
    let creativeShotCountCol = 0;
    if (creativeShotDateWord != "" & creativeImgNumWord != "") {
      creativeShotDateCol = brandShotlist.createTextFinder(creativeShotDateWord).matchEntireCell(true).findNext().getColumn() - 1;
      creativeShotCountCol = brandShotlist.createTextFinder(creativeImgNumWord).matchEntireCell(true).findNext().getColumn() - 1;
    };

    brandReports[brand] = {};
    const prodShotArr = [];
    const modelShotArr = [];
    const creativeShotArr = [];
    const prodUnshotArr = {"Flatlay": [], "Tabletop": [], "Mannequin": [], "Creative": []};
    let totalEcomShotCount = 0;
    //let totalModelShotCount = 0;
    // let totalCreativeShotCount = 0;

    for (let i = headerRow; i < lastRow; i++) {
      const shootNoteCell = brandShotlistData[i][shootNoteCol];
      const recDateCell = brandShotlistData[i][recDateCol];
      const ecomShotDateCell = brandShotlistData[i][ecomShotDateCol];
      if (modelShotDateCol != 0) {
        const modelShotDateCell = brandShotlistData[i][modelShotDateCol];
      } else if (creativeShotDateCol != 0) {
        const creativeShotDateCell = brandShotlistData[i][creativeShotDateCol];
      };
      //products shot & img count
      if (shootNoteCell != dnsWord & recDateCell != "" & ecomShotDateCell != "") {
        const productShot = brandShotlistData[i][prodCol];
        prodShotArr.push(productShot);
        const productShotCount = brandShotlistData[i][ecomShotCountCol];
        totalEcomShotCount += parseInt(productShotCount);
      //products that only needs model shot (to avoid falling to unshot cat)
      } else if (shootNoteCell == modelShootNoteWord & modelShotDateCol != 0) {
        const modelShot = brandShotlistData[i][prodCol];
        modelShotArr.push(modelShot);
        //const modelShotCount = brandShotlistData[i][modelShotCountCol];
        //totalModelShotCount += parseInt(modelShotCount);
      //products received but unshot
      } else if (shootNoteCell == creativeShootNoteWord & creativeShotDateCol != 0) {
        const creativeShot = brandShotlistData[i][prodCol];
        creativeShotArr.push(creativeShot);
        //const creativeShotCount = brandShotlistData[i][creativeShotCountCol];
        //totalCreativeShotCount += parseInt(creativeShotCount);
      //products received but unshot
      } else if (shootNoteCell != dnsWord & recDateCell != "" & ecomShotDateCell == "") {
        const productUnshot = brandShotlistData[i][prodCol];
        if (shootNoteCell.includes(flatlayWord)) {
          prodUnshotArr["Flatlay"].push(productUnshot);
        } else if (shootNoteCell.includes(tabletopWord)) {
          prodUnshotArr["Tabletop"].push(productUnshot);
        } else if (shootNoteCell.includes(mannequinWord)) {
          prodUnshotArr["Mannequin"].push(productUnshot);
        };
      };
    };
    const prodUnshotNum = prodUnshotArr["Flatlay"].length + prodUnshotArr["Tabletop"].length + prodUnshotArr["Mannequin"].length;

    brandReports[brand]["Products Shot"] = prodShotArr;
    brandReports[brand]["Model Shot"] = modelShotArr;
    brandReports[brand]["Unshot Products List"] = prodUnshotArr;
    brandReports[brand]["Products Unshot"] = prodUnshotNum;
    brandReports[brand]["Flatlay Unshot"] = prodUnshotArr["Flatlay"].length;
    brandReports[brand]["Tabletop Unshot"] = prodUnshotArr["Tabletop"].length;
    brandReports[brand]["Mannequin Unshot"] = prodUnshotArr["Mannequin"].length;
    brandReports[brand]["Total Images Shot"] = totalEcomShotCount;

    const brandData = [brand, '', prodUnshotArr["Flatlay"].length, prodUnshotArr["Tabletop"].length, prodUnshotArr["Mannequin"].length, prodUnshotNum, url];
    brandReportsData.push(brandData);
  };

  //format header
  const reportSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Brand Summary');
  reportSheet.getDataRange().clear();
  const unshotMergeHeader = reportSheet.getRange('D2:G2').merge().setValue('Unshot Products');
  const repHeaderRow = reportSheet.getRange('B3:H3');
  const repHeaders = [['Brand', 'Products Shot Ytd', 'Flatlay', 'Tabletop', 'Mannequin', 'Brand Total', 'URL']];
  repHeaderRow.setValues(repHeaders);

  //write data
  const rangeToWriteLastRow = (sourceActiveBrandList.length + 3);
  const repRangeToWrite = reportSheet.getRange('B4:H' + rangeToWriteLastRow.toString());
  repRangeToWrite.setValues(brandReportsData);

  //write toal
  function getTotalEle(ele) {
    //function to get each of the shoot type no.
    const eleValues = Object.keys(brandReports).map(key => brandReports[key][ele]);
    Logger.log('eleValues: ' + eleValues);
    let totalEle = 0;
    for (let i = 0; i < eleValues.length; i++) {
      totalEle += eleValues[i];
    };
    return totalEle;
  };
  const dateCell = 'Updated On: ' + new Date();
  const totalData = [['Total', '', getTotalEle('Flatlay Unshot'), getTotalEle('Tabletop Unshot'), getTotalEle('Mannequin Unshot'), getTotalEle('Products Unshot'), dateCell]];
  const totalRangeRow = rangeToWriteLastRow + 1;
  const totalRangeToWrite = reportSheet.getRange('B' + totalRangeRow.toString() + ':H' + totalRangeRow.toString()); //columns might change
  totalRangeToWrite.setValues(totalData);

  //formatting
  reportSheet.getDataRange().setWrap(true).setFontFamily('Avenir').setFontSize('10').setHorizontalAlignment('center');
  unshotMergeHeader.setBackground('#ff6f31').setFontColor('#ffffff').setFontSize('12');
  repHeaderRow.setFontColor('#ffffff').setFontSize('12');
  reportSheet.getRange('B3').setBackground('#1c7685');
  reportSheet.getRange('C3').setBackground('#1c7685');
  reportSheet.getRange('D3:H3').setBackground('#004561');
  repRangeToWrite.setBackground('#c1dfe5').setFontColor('#000000');
  reportSheet.getRange('C3').setBackground('#57bb8a');
  totalRangeToWrite.setBackground('#b2cfd5').setFontColor('#000000');
};



/*
Check Amendment
*/

function checkAmendment() {

  SpreadsheetApp.flush();

  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Outstanding Amendment');

  //reset the background colour
  sheet.getDataRange().setBackground('#f3f3f3').setHorizontalAlignment('center');

  const brandTrackers = {
    'Agnes b': 'https://docs.google.com/spreadsheets/d/1rC1-voiH3NYIsFgi3VsoWd0ds7ojZGw084XI3M6J8po/edit#gid=1601560151',
    'AIWA': 'https://docs.google.com/spreadsheets/d/10GJTYf3yfBpnxR69j1gcnfxi1u6AYfvtGfmD6w4Oyus/edit#gid=970161406',
    'Arena': 'https://docs.google.com/spreadsheets/d/10yNTABlFQlx_R7nbqR3oXii40rFwzsw8IajwR0V5ftE/edit#gid=1684687137',
    'Esprit': 'https://docs.google.com/spreadsheets/d/1LK_Quoa7yJsEiL8yV01wBn8c1EOJFEMB_886atckwvc/edit#gid=210531185',
    'Fred Perry': 'https://docs.google.com/spreadsheets/d/1y4JI-a44SjZiBcW94G5J8GErm1ytKMPC13YKhlXcb1M/edit#gid=949243280',
    'New Balance': 'https://docs.google.com/spreadsheets/d/10D_KgKpsYesrY6xzTQpb2ZvmR9NoFO32GGtlhjjA-U0/edit#gid=863564986',
    'OnTheList': 'https://docs.google.com/spreadsheets/d/1AqX784_9lpP9WGgddLLdmOskHseAB2rgL98o3jefggA/edit#gid=259185547',
    'Petit Bateau': 'https://docs.google.com/spreadsheets/d/1aSYGtTLBjaqJBA6owQALhb4L_achp11b2Gjic3cQtwE/edit#gid=1637937787',
    'Toy R US': 'https://docs.google.com/spreadsheets/d/1H1gtR3nceJJUh73JKCV4Xx1GJpuZkhHvfMeUwFR83bw/edit#gid=1459237771',
    'WEAT': 'https://docs.google.com/spreadsheets/d/150j8-pMeSv4N1Fr4ZmQnjixwpcqIAbUOE2Sn1HCCrWc/edit#gid=1993904249'
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
  sheet.getRange('B2').setBackground('#004561').setFontColor('#ffffff');
  sheet.getRange('B3').setBackground('#ffffff').setFontColor('#ff6f31');
  sheet.getRange('C3:D3').setBackground('#ff6f31').setFontColor('#ffffff');
  sheet.getRange('B4:B' + numRow.toString()).setBackground('#1c7685').setFontColor('#ffffff');
  sheet.getRange('C4:D' + numRow.toString()).setBackground('#c1dfe5').setFontColor('#004561');

  //update the Outstanding Amendments sheet
  range.setValues(amendmentInfo);

  //GUI alert to display brands with outstanding amendments
  SpreadsheetApp.getUi().alert(msg);

};
