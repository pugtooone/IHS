//Google Apps Script for Google Sheet autofill dates based on edit trigger

/** @OnlyCurrentDoc */
function onEdit(e) {

  const eValue = e.range.getValue();
  const eColumn = e.range.getColumn();
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const reqDateCell = ss.getRange("Amendment Tracker!B2");
  const reqDateCol = reqDateCell.getColumn();
  const deliDateCell = ss.getRange("Amendment Tracker!K2");
  const deliDateCol = deliDateCell.getColumn();
  const shipBackDateCell = ss.getRange("Shot List!Q2");
  const shipBackDateCol = shipBackDateCell.getColumn();

//Amendment Tracker Autofill Dates
  if (ss.getSheetName() === "Amendment Tracker") {

    if (eColumn == reqDateCol + 3  && eValue !== "") {

      const cell = e.range.offset(0, -3);
      
      if (cell.getValue() === "" && cell.getRow() > 2 && reqDateCell.getValue() === "Request Date" && cell.getColumn() === reqDateCol) {
        cell.setValue(new Date());
      }

    } else if (eColumn == deliDateCol - 1  && eValue !== "") {

      const cell = e.range.offset(0, 1);

      if (cell.getValue() === "" && cell.getRow() > 2 && deliDateCell.getValue() === "Delivery Date" && cell.getColumn() === deliDateCol) {
        cell.setValue(new Date());
      }

    };

  };

//Shotlist Autofill Ship Back Date
  if (ss.getSheetName() === "Shot List") {

    if (eColumn == shipBackDateCol - 1  && eValue === "Shipped back") {

      const cell = e.range.offset(0, 1);

      if (cell.getValue() === "" && cell.getRow() > 2 && shipBackDateCell.getValue() === "Ship Back Date" && cell.getColumn() === shipBackDateCol) {
       cell.setValue(new Date());
      };
    };

  };

}
