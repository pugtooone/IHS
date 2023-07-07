/** @OnlyCurrentDoc */

function timeTrackingSummary() {

  //getting the URLs of each staff's Time Tracking sheet
  const trackFolder = DriveApp.getFoldersByName("Staff Time Tracking").next();
  const trackFilesIter = trackFolder.getFiles();
  let trackFileUrls = [];
  while (trackFilesIter.hasNext()){
    const file = trackFilesIter.next();
    if (!file.getName().startsWith("[Sample]")) {
      const url = file.getUrl();
      trackFileUrls.push(url);
    };
  };

  //constructing the tab name to be searched in each sheet (current month)
  const currentDate = new Date();
  const currentMonth = currentDate.getMonth();
  const currentYear = currentDate.getFullYear() - 2000;
  const monthList = {0: "Jan", 1: "Feb", 2: "Mar", 3: "Apr", 4: "May", 5: "Jun", 6: "Jul", 7: "Aug", 8: "Sep", 9: "Oct", 10: "Nov", 11: "Dec"};
  const tabName = monthList[currentMonth] + currentYear.toString();

  let reportObj = {};

  for (let url of trackFileUrls) {
    let brandObj = {};

    const employeeSheet = SpreadsheetApp.openByUrl(url).getSheetByName(tabName);
    const employeeName = employeeSheet.createTextFinder("Employee Name:").matchEntireCell(true).findNext().offset(0, 1).getValue();
    let employeeObj = reportObj[employeeName] = {};
    const roleObj = {"Stockroom": "Stockroom", "Styli": "Styling", "Photographer": "Photography", "Image": "QC", "Studio": "Studio"}; //setting: search the substring to map the department
    const jobTitle = employeeSheet.createTextFinder('Role:').matchEntireCell(true).findNext().offset(0, 1).getValue().toString();
    for (let substr of Object.keys(roleObj)) {
      if (jobTitle.search(substr) != -1) {
        const role = roleObj[substr];
        Logger.log(`${employeeName} works in ${role}`);
        employeeObj["role"] = role;
        break;
      };
    };


    const brandKeyRow = employeeSheet.createTextFinder("Client Name").matchEntireCell(true).findNext().getRow();
    const brandKeyCol = employeeSheet.createTextFinder("Client Name").matchEntireCell(true).findNext().getColumn();
    const totalCells = employeeSheet.createTextFinder("TOTAL").matchEntireCell(true).findAll();
    let totalCol = 0;
    let totalRow = 0;
    for (let total of totalCells) {
      const thisTotalCol = total.getColumn();
      const thisTotalRow = total.getRow();
      thisTotalCol > totalCol ? totalCol = thisTotalCol : totalCol = totalCol;
      thisTotalRow > totalRow ? totalRow = thisTotalRow : totalRow = totalRow;
    };

    for (let i = brandKeyRow + 1; i < totalRow; i++) {
      const brand = employeeSheet.getRange(i, brandKeyCol).getValue();
      if (brand !== "") {
        const numWorkHourPerBrand = employeeSheet.getRange(i, totalCol).getValue();
        brandObj[brand] = numWorkHourPerBrand;
      };
    };

    reportObj[employeeName]["brand"] = brandObj;

  };
  
  const prettyReportObj = JSON.stringify(reportObj, null, 2);
  Logger.log(prettyReportObj);

  //constructing reporting format
  const employeeList = Object.keys(reportObj).sort();
  let brandList = [];
  for (let employee of employeeList) {
    const employeeBrandList = Object.keys(reportObj[employee]["brand"]);
    brandList = brandList.concat(employeeBrandList);
  };

  //convert the employeeList to column format
  const employeeListToCol = employeeList.map(value => [value]);
  //remove the duplicated brand
  const deDupBrandList = [...new Set(brandList)];
  //remove the general studio stuff from the array, and add to the back for better reporting
  const studioStuff = ['Studio', 'Holidays', 'Sickness'];
  Logger.log('Before: ' + deDupBrandList)
  for (let stuff of studioStuff) {
    deDupBrandList.splice(deDupBrandList.indexOf(stuff), 1);
    deDupBrandList.push(stuff);
    Logger.log('After: ' + deDupBrandList);
  };

  //Summary Sheet
  const sumSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Time Tracking Summary");
  sumSheet.insertColumns(sumSheet.getMaxColumns(), 22); //inserting columns to the end
  const endCellList = sumSheet.createTextFinder("End").findAll();
  let endCellCol = 0;
  if (endCellList != null) {
    for (let endCell of endCellList) {
      if (endCell.getColumn() > endCellCol) {
        endCellCol = endCell.getColumn();
      };
    };
  };

  const startCell = sumSheet.getRange(2, endCellCol + 2);
  //the new range for this month data to be written in, if not create, previous brand or employee name will be matched with text finder
  const newRangeToWrite = sumSheet.getRange(startCell.getRow(), startCell.getColumn(), sumSheet.getMaxRows() - startCell.getRow(), sumSheet.getMaxColumns() - startCell.getColumn());
  const header = sumSheet.getRange(startCell.getRow(), startCell.getColumn(), 1, deDupBrandList.length + 2).merge().setValue(tabName).setBackground('#004562').setFontColor('#efefef').setFontSize(12).setHorizontalAlignment('center').setVerticalAlignment('middle');
  const writeEndCell = header.offset(0, 1).setValue('End').setBackground('#004562').setFontColor('#efefef').setHorizontalAlignment('center').setVerticalAlignment('middle');

  const roleCell = sumSheet.getRange(startCell.getRow() + 1, startCell.getColumn(), 1, 2).merge().setValue("Role").setBackground("#ffffff").setFontColor("#004562").setHorizontalAlignment("center");
  const headerRowRange = sumSheet.getRange(startCell.getRow() + 1, startCell.getColumn() + 2, 1, deDupBrandList.length).setBackground('#ff6f31').setFontColor('#efefef').setHorizontalAlignment('center');
  headerRowRange.setValues([deDupBrandList]);

  const employeeColRange = sumSheet.getRange(headerRowRange.getRow() + 1, startCell.getColumn() + 1, employeeListToCol.length, 1).setBackground('#1d7685').setFontColor('#efefef');
  employeeColRange.setValues(employeeListToCol);

  for (let employee of employeeList) {
    newRangeToWrite.createTextFinder(employee).matchEntireCell(true).findNext().offset(0, -1).setValue(reportObj[employee]["role"]).setBackground("#b7e1cd").setFontColor("#004562");
    for (let brand of Object.keys(reportObj[employee]["brand"])) {
      if( reportObj[employee]["brand"][brand] != 0) {
        const toWriteRow = newRangeToWrite.createTextFinder(employee).matchEntireCell(true).findNext().getRow();
        const toWriteCol = newRangeToWrite.createTextFinder(brand).matchEntireCell(true).findNext().getColumn();
        sumSheet.getRange(toWriteRow, toWriteCol).setValue(reportObj[employee]["brand"][brand]);
      };
    };
  };

  //setting sum formulas
  const brandTotalCell = sumSheet.getRange(employeeColRange.getLastRow() + 1, startCell.getColumn(), 1, 2).merge().setValue('Brand Total').setBackground('#004562').setFontColor('#efefef');
  const brandTotalRow = sumSheet.getRange(employeeColRange.getLastRow() + 1, startCell.getColumn() + 2, 1, deDupBrandList.length + 1).setBackground('#b2cfd5').setFontColor('');
  const brandSumFormula = `=SUM(R[-${employeeList.length}]C[0]:R[-1]C[0])`;
  const brandSumFormulas = [];
  for (let i = 0; i < deDupBrandList.length + 1; i++) brandSumFormulas.push(brandSumFormula);
  brandTotalRow.setFormulasR1C1([brandSumFormulas]);

  const employeeTotalCell = sumSheet.getRange(headerRowRange.getRow(), headerRowRange.getLastColumn() + 1).setValue('Employee Total').setBackground('#ff6f31').setFontColor('#efefef').setHorizontalAlignment('center');
  const employeeTotalCol = sumSheet.getRange(headerRowRange.getRow() + 1, headerRowRange.getLastColumn() + 1, employeeList.length, 1).setBackground('#b2cfd5').setFontColor('#004562');
  const employeeSumFormula = `=SUM(R[0]C[-${deDupBrandList.length}]:R[0]C[-1])`;
  const employeeSumFormulas = [];
  for (let i = 0; i < employeeList.length; i++) employeeSumFormulas.push([employeeSumFormula]);
  employeeTotalCol.setFormulasR1C1(employeeSumFormulas);

  const numberRange = sumSheet.getRange(headerRowRange.getRow() + 1, employeeColRange.getColumn() + 1, employeeList.length, deDupBrandList.length).setBackground('#c1dfe5').setFontColor('#004562');

  const brandNotShot = brandTotalRow.createTextFinder('0').matchEntireCell(true).findAll();
  for (range of brandNotShot.reverse()) {
    const col = range.getColumn();
    sumSheet.deleteColumn(col);
  };
}
