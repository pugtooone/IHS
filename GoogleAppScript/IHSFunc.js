/*

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
    .addItem('Integrate Shotlists', 'integrateShotlists')
    .addToUi();
};

function integrateShotlists() {

  SpreadsheetApp.flush();

  const sourceSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Brand Status');

  //get the coordinates for header "Brand"
  const brandRange = sourceSheet.createTextFinder('Brand').matchEntireCell(true).findNext();
  const brandRow = brandRange.getRow();
  const brandCol = brandRange.getColumn();

  //mapping the source header with the col num
  const sourceHeader = sourceSheet.getRange(brandRow, brandCol, 1, 19).getValues(); //setting: change 4th argument
  const sourceHeaderObj = {};
  for (let i = 0; i < sourceHeader[0].length; i++) {
    const header = sourceHeader[0][i];
    const col = brandCol + i;
    sourceHeaderObj[header] = col;
  };

  //logging the brand source
  const prettySourceHeaderObj =JSON.stringify(sourceHeaderObj, null, 2);
  Logger.log(prettySourceHeaderObj);

  const brandObj = {};

  const sourceActiveBrandList = sourceSheet.createTextFinder('Active').matchEntireCell(true).findAll(); //getting the range of all 'Active' cells
  
  //defining global variable for kipling
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
 
  Logger.log('No. of Active Brands: ' + sourceActiveBrandList.length);
  const prettyBrandObj = JSON.stringify(brandObj, null, 2);
  Logger.log('Received Unshot: \n' + prettyBrandObj);

//=======================================================================================================================================================================================
// Est Unshot Products
//=======================================================================================================================================================================================

  const estSourceSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Est Product Delivery');
  const estBrandCol = estSourceSheet.createTextFinder('Brand').matchEntireCell(true).findNext().getColumn();
  const estBrandRow = estSourceSheet.createTextFinder('Brand').matchEntireCell(true).findNext().getRow();
  const estShootTypeCol = estSourceSheet.createTextFinder('Shoot Type').matchEntireCell(true).findNext().getColumn();
  const estNumProdCol = estSourceSheet.createTextFinder('No. of Products').matchEntireCell(true).findNext().getColumn();
  const receivedNumProdCol = estSourceSheet.createTextFinder('No. of Recived Products').matchEntireCell(true).findNext().getColumn();
  const receivedStatusCol = estSourceSheet.createTextFinder('Received').matchEntireCell(true).findNext().getColumn();

  let estBrandObj = {};
  for (let i=0; i<estSourceSheet.getLastRow(); i++) {
    const brand = estSourceSheet.getRange(estBrandRow + 1 + i, estBrandCol).getValue();
    const receivedStatus = estSourceSheet.getRange(estBrandRow + 1 + i, receivedStatusCol).getValue();
    if (brand == '') {
      break;
    } else if (receivedStatus == 'TRUE') {
      continue;
    };
    (!estBrandObj[brand]) ? estBrandObj[brand] = {}: {}; //init estBrandObj[brand] as {}
    const shootType = estSourceSheet.getRange(estBrandRow + 1 + i, estShootTypeCol).getValue();
    const estNumProd = estSourceSheet.getRange(estBrandRow + 1 + i, estNumProdCol).getValue();
    let receivedNumProd = estSourceSheet.getRange(estBrandRow + 1 + i, receivedNumProdCol).getValue();
    receivedNumProd == '' ? receivedNumProd = 0 : {}; //if no item is received, change the value to 0 instead of ''
    const outstandingEstNumProd = estNumProd - receivedNumProd;
    if (estBrandObj[brand][shootType]) {
      estBrandObj[brand][shootType] += outstandingEstNumProd;
    } else {
      estBrandObj[brand][shootType] = outstandingEstNumProd;
    };
  };

  const prettyEstBrandObj = JSON.stringify(estBrandObj, null, 2);
  Logger.log('Est Product Deliver: \n' + prettyEstBrandObj);

//=======================================================================================================================================================================================
// Building Brand Report
//=======================================================================================================================================================================================

  //construct brand report for received but unshot
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
    //let totalCreativeShotCount = 0;

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

    let estFlatlay = brandReports[brand]["Est Flatlay"] = 0;
    let estTabletop = brandReports[brand]["Est Tabletop"] = 0;
    let estBust = brandReports[brand]["Est Mannequin"] = 0;

    if (estBrandObj[brand] != null) {
      for (let category of Object.keys(estBrandObj[brand])) {
        switch (category) {
          case "Flatlay":
            estFlatlay += estBrandObj[brand][category];
            Logger.log(brand + 'Flatlay: ' + estFlatlay);
            break;
          case "Standing Flatlay":
            estFlatlay += estBrandObj[brand][category];
            Logger.log(brand + 'Flatlay: ' + estFlatlay);
            break;
          case "Tabletop":
            estTabletop += estBrandObj[brand][category];
            Logger.log(brand + 'Tabletop: ' + estTabletop);
            break;
          case "Mannequin":
            estBust += estBrandObj[brand][category];
            Logger.log(brand + ' Bust: ' + estBust);
            break;
          default:
            Logger.log(`This is not a est Ecom batch: ${brand} ${category}`);
        };
      };
    };

    const brandData = [brand, '', '', prodUnshotArr["Flatlay"].length, prodUnshotArr["Tabletop"].length, prodUnshotArr["Mannequin"].length, '', estFlatlay, estTabletop, estBust, '', '', url]; //setting
    let realBrandData = brandData.map(ele => (ele == 0 ? "": ele));
    brandReportsData.push(realBrandData);
  };

  //append Kipling data to brandReportsData if Kipling is active
  if (kiplingCell != null) {
    let estKipTabletop = 0;
    for (let category of Object.keys(estBrandObj["Kipling"])) {
        switch (category) {
          case "Tabletop":
            estKipTabletop += estBrandObj["Kipling"][category];
            Logger.log('Kipling Tabletop: ' + estKipTabletop);
            break;
          default:
            Logger.log(`This is not a est Ecom batch: Kipling ${category}`);
        };
      };
    const kipData = ['Kipling', '', '', '', 'Check Teams', '', '', '', estKipTabletop, '', '', '', 'Microsoft Teams']; //setting
    brandReportsData.push(kipData);
  };

//=======================================================================================================================================================================================

  //format header
  const reportSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Production Summary');
  reportSheet.getDataRange().clear().setBackground("#ffffff");
  const mergeHeader = reportSheet.getRange('B2:N2').merge().setValue('Production Summary'); //setting
  const repHeaderRow = reportSheet.getRange('B3:N3'); //setting
  const repHeaders = [['Brand', 'Products Shot Ytd', 'Products need Reshoot', 'Received Unshot Flatlay', 'Received Unshot Tabletop', 'Received Unshot Mannequin', 'Received Total', 'Est Delivering Flatlay', 'Est Delivering Tabletop', 'Est Delivering Mannequin', 'Est Total', 'Grand Total','URL']]; //setting
  repHeaderRow.setValues(repHeaders);

//=======================================================================================================================================================================================

  //write data
  const rangeToWriteFirstRow = 4; //first brand data start from B4
  const rangeToWriteLastRow = (sourceActiveBrandList.length + 3);
  const rangeToWriteFirstCol = 2;
  const rangeToWriteLastCol = repHeaders[0].length;
  const repRangeToWrite = reportSheet.getRange(rangeToWriteFirstRow, rangeToWriteFirstCol, sourceActiveBrandList.length, rangeToWriteLastCol);
  repRangeToWrite.setValues(brandReportsData);

  /*
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
  */

  //write to Totals
  const brandCell = reportSheet.createTextFinder('Brand').findNext();
  const brandCellRow = brandCell.getRow();
  const brandCellCol = brandCell.getColumn();
  reportSheet.getRange(rangeToWriteLastRow + 1, brandCellCol).setValue('Total');
  const totalCellRow = reportSheet.createTextFinder('Total').matchEntireCell(true).findNext().getRow();
  const urlCellCol = reportSheet.createTextFinder('URL').matchEntireCell(true).findNext().getColumn();
  const receivedTotalCol = reportSheet.createTextFinder('Received Total').findNext().getColumn();
  const estTotalCol = reportSheet.createTextFinder('Est Total').findNext().getColumn();
  const grandTotalCol = reportSheet.createTextFinder('Grand Total').findNext().getColumn();

  const dateCellData = 'Updated On: ' + new Date();
  reportSheet.getRange(totalCellRow, urlCellCol).setValue(dateCellData);

  //write to Total row
  for (let i = brandCellCol + 1; i < urlCellCol -2 ; i++) {
    const totalCell = reportSheet.getRange(`R${totalCellRow}C${i}`);
    totalCell.setFormulaR1C1(`=SUM(R[-${totalCellRow - brandCellRow-1}]C[0]:R[-1]C[0])`)
  }

  //write to Receivd & Est & Grand total cols
  for (let i = brandCellRow + 1; i < totalCellRow + 1; i++) {
    const receivedTotalCell = reportSheet.getRange(`R${i}C${receivedTotalCol}`);
    receivedTotalCell.setFormulaR1C1(`=SUM(R[0]C[-3]:R[0]C[-1])`);
    const estTotalCell = reportSheet.getRange(`R${i}C${estTotalCol}`);
    estTotalCell.setFormulaR1C1(`=SUM(R[0]C[-3]:R[0]C[-1])`);
    const grandTotalCell = reportSheet.getRange(`R${i}C${grandTotalCol}`);
    grandTotalCell.setFormulaR1C1(`=R[0]C[-${grandTotalCol - receivedTotalCol}] + R[0]C[-${grandTotalCol - estTotalCol}]`);
  };

/*
  //remove zeros
  for (i=rangeToWriteFirstRow; i<rangeToWriteLastRow + 1; i++) {
    for (j=rangeToWriteFirstCol; j<rangeToWriteLastCol + 1; j++) {
      if (reportSheet.getRange(i, j).getValue() === 0) {
        reportSheet.getRange(i, j).clear();
      };
    };
  };
*/

//========================================================================================================================================================================================

  //formatting
  const prodShotYtdCol = reportSheet.createTextFinder('Products Shot Ytd').matchEntireCell(true).findNext().getColumn();
  const prodNeedReshootCol = reportSheet.createTextFinder('Products need Reshoot').matchEntireCell(true).findNext().getColumn();

  reportSheet.getDataRange().setWrap(true).setFontFamily('Avenir').setFontSize('10').setHorizontalAlignment('center').setBackground('#f3f3f3').setBorder(false, false, false, false, false, false);
  mergeHeader.setBackground('#004561').setFontColor('#f3f3f3').setFontSize('14');
  repHeaderRow.setBackground('#ff6f31').setFontColor('#f3f3f3').setFontSize('12');
  brandCell.setBackground('#ffffff').setFontColor('#ff6f31').setFontSize('12');
  repRangeToWrite.setBackground('#c1dfe5').setFontColor('#004561');
  reportSheet.getRange(totalCellRow, rangeToWriteFirstCol, 1, repHeaders[0].length).setBackground('#b2cfd5').setFontColor('#004561'); //Total row
  reportSheet.getRange(rangeToWriteFirstRow, rangeToWriteFirstCol, sourceActiveBrandList.length + 1).setBackground('#1c7685').setFontColor('#f3f3f3'); //Brands
  reportSheet.getRange(rangeToWriteFirstRow, prodShotYtdCol, sourceActiveBrandList.length + 1).setBackground('#b2cfd5').setFontColor('#004561'); //Products Shot Ytd
  reportSheet.getRange(brandCellRow, prodShotYtdCol).setBackground('#1c7685').setFontColor('#f3f3f3');
  reportSheet.getRange(rangeToWriteFirstRow, prodNeedReshootCol, sourceActiveBrandList.length + 1).setBackground('#b2cfd5').setFontColor('#004561'); //Products need Reshoot
  reportSheet.getRange(brandCellRow, prodNeedReshootCol).setBackground('#1c7685').setFontColor('#f3f3f3');
  reportSheet.getRange(rangeToWriteFirstRow, receivedTotalCol, sourceActiveBrandList.length + 1).setBackground('#b2cfd5').setFontColor('#004561'); //Received Total
  reportSheet.getRange(rangeToWriteFirstRow, estTotalCol, sourceActiveBrandList.length + 1).setBackground('#b2cfd5').setFontColor('#004561'); //Est Total
  reportSheet.getRange(rangeToWriteFirstRow, grandTotalCol, sourceActiveBrandList.length + 1).setBackground('#88a3a8').setFontColor('#004561'); //Grand Total
  reportSheet.getRange(rangeToWriteFirstRow, urlCellCol, sourceActiveBrandList.length + 1).setBackground('#1c7685').setFontColor('#f3f3f3'); //URL
  reportSheet.getRange(totalCellRow, urlCellCol).setBackground('#004561').setFontColor('#f3f3f3');
  reportSheet.getRange(rangeToWriteFirstRow, rangeToWriteFirstCol + 1, sourceActiveBrandList.length + 1, repHeaders[0].length - 1).setBorder(false, false, false, false, false, true, "#004561", SpreadsheetApp.BorderStyle.SOLID);

  //resize columns
  reportSheet.setColumnWidths(1, reportSheet.getLastColumn(), 100);
  const urlColNum = reportSheet.createTextFinder('URL').findNext().getColumn();
  reportSheet.setColumnWidth(urlColNum, 500);

  Logger.log('finish');
};

//EOF======================================================================================================================================================================================
