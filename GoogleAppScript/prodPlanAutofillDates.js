/* event-triggered function for Production Plan to auto-fill dates for
    1. "Actual 1st Delivery Date" when any job is delivered
    2. "Job Create Date" when any job is created
*/

/** @OnlyCurrentDoc */
function onEdit(e) {

  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('2023');
  const jobStatusCol =sheet.createTextFinder('Job Status').findNext().getColumn();
  const deliDateCol =sheet.createTextFinder('Actual 1st Delivery Date').findNext().getColumn();
  const jobCreateDateCol =sheet.createTextFinder('Job Create Date').findNext().getColumn();
  const jobNumCol =sheet.createTextFinder('Job Number').findNext().getColumn();
  const eOldValue = e.oldValue;
  const eValue =e.range.getValue();
  const eCol = e.range.getColumn();
  const eRow = e.range.getRow();

  //fill the Delivery date
  if (eCol == jobStatusCol && eValue === "Delivered") {
    const cell = sheet.getRange(eRow, deliDateCol);
    if (cell.getValue() === "") {
     cell.setValue(new Date());
    };
  };

  //fill the job create date if any of the job number is added
  if (eCol == jobNumCol && eValue != "" && eOldValue == null) {
    const cell = sheet.getRange(eRow, jobCreateDateCol);
    if (cell.getValue() === "") {
      cell.setValue(new Date());
    };
  };

};
