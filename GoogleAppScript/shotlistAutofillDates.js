//Google Apps Script for Google Sheet autofill dates based on edit trigger

/** @OnlyCurrentDoc */
function onEdit(e) {

  const eValue = e.range.getValue();
  const eCol = e.range.getColumn();
  const eRow = e.range.getRow();

  const mainShotlist = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Shot List');
  const shipBackDateCol = mainShotlist.createTextFinder('Ship Back Date').matchEntireCell(true).findNext().getColumn();
  const checkouteCol = mainShotlist.createTextFinder('Check Out IHS').matchEntireCell(true).findNext().getColumn();
  const shipBackWord = "Shipped back"; //text of the checkout status

  const amendTrackerSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Amendment Tracker');
  const reqDateCol = amendTrackerSheet.createTextFinder('Request Date').matchEntireCell(true).findNext().getColumn();
  const deliDateCol = amendTrackerSheet.createTextFinder('Delivery Date').matchEntireCell(true).findNext().getColumn();
  const imgCol = amendTrackerSheet.createTextFinder('Image Name').matchEntireCell(true).findNext().getColumn();
  const linkCol = amendTrackerSheet.createTextFinder('Delivery Link').matchEntireCell(true).findNext().getColumn();

  //Shotlist Autofill Ship Back Date
  if (eCol === checkouteCol && eValue === shipBackWord) {
    const cell = mainShotlist.getRange(eRow, shipBackDateCol);
    if (cell.getValue() === "") {
     cell.setValue(new Date());
    };
  };

  //Amendment Tracker Autofill Dates
  if (eCol === imgCol  && eValue !== "") {
    const cell = amendTrackerSheet.getRange(eRow, reqDateCol);
    if (cell.getValue() === "" && cell.getRow() > 2) {
     cell.setValue(new Date());
    }
  } else if (eCol === linkCol && eValue !== "") {
    const cell = amendTrackerSheet.getRange(eRow, deliDateCol);
    if (cell.getValue() === "" && cell.getRow() > 2) {
     cell.setValue(new Date());
    }
  };

}
