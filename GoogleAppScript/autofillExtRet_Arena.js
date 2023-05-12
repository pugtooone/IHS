/** @OnlyCurrentDoc */
function onOpen(e) {
  const shotList = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Shotlist");
  const tracker = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Amendment Tracker");

  //construct a product list with extensive retouch
  const trackerSKUCol = tracker.createTextFinder('SKU Name').findNext().getColumn(); //get the column of "SKU Name"
  const extRetList = tracker.createTextFinder('EXTENSIVE RETOUCH').findAll(); //return ranges of all "EXTENSIVE RETOUCH", which later used for getting the row
  const extRetSKUList = [];
  for (let i = 0; i < extRetList.length; i++) {
    SKU = tracker.getRange(extRetList[i].getRow(), trackerSKUCol).getValue();
    extRetSKUList.push(SKU);
  };
  const realExtRetSKUList = [...new Set(extRetSKUList)]; //rm duplicates
  const realExtRetSKUListPP = JSON.stringify(realExtRetSKUList, null, 2);
  Logger.log('Products with Ext Ret:\n' + realExtRetSKUListPP);

  const shotlistSKUCol = shotList.createTextFinder("SKU").findNext().getColumn();
  const amendCol = shotList.createTextFinder('Amendment').findNext().getColumn();
  const shotListLastRow = shotList.getLastRow();

  const rangeToWrite = shotList.getRange(3, amendCol, shotListLastRow - 2);
  rangeToWrite.clear({contentsOnly: true});
  Logger.log('Cleaning cells: ' + rangeToWrite.getA1Notation());

  for (let i = 0; i < realExtRetSKUList.length; i++) {
    const rowToWrite = shotList.createTextFinder(realExtRetSKUList[i]).findNext().getRow();
    const cellToWrite = shotList.getRange(rowToWrite, amendCol);
    cellToWrite.setValue("Extensive Retouch");
    Logger.log('Writing to: ' + realExtRetSKUList[i] + '--' + cellToWrite.getA1Notation());
  };
};
