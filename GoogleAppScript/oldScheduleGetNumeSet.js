function getNumSet() {

  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheetsList = ss.getSheets();
  let octToDecList = [];
  //constructing list of sheets in Oct to Dec
  for (let sheet of sheetsList) {
    const sheetName = sheet.getName();
    if ( sheetName.includes('Oct') || sheetName.includes('Nov') || sheetName.includes('Dec') ) {
      octToDecList.push(sheet);
    };
  };

  const prettyOctToDecList = JSON.stringify(octToDecList.map(sheet => sheet.getName()), null, 2);
  Logger.log(`List of Oct to Dec Sheets:\n\n${prettyOctToDecList}`);

  let totalSets = 0;

  for (let sheet of octToDecList) {
    let sheetSets = 0;
    const targetLastRow = sheet.createTextFinder('Creative 4 - On Site').matchEntireCell(true).findNext().getRow();
    const photogColList = sheet.createTextFinder('Photographer'). matchEntireCell(true).findAll();

    for (let photogCol of photogColList) {
      const searchRange = sheet.getRange(4, photogCol.getColumn(), targetLastRow - 4 + 1);
      const cellValues = searchRange.getValues();
      //Logger.log(`search range: ${searchRange.getA1Notation()}`)
      Logger.log(`cell values: ${cellValues}`)
      for (let cell of cellValues) {
        if ( cell != "" ) {
          Logger.log(`Photographer: ${cell}`)
          sheetSets += 1;
        };
      };
    };
    totalSets += sheetSets;
  };

  Logger.log(totalSets);
}

