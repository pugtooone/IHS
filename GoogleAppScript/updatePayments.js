/** @OnlyCurrentDoc */
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  // Or DocumentApp or FormApp.
  ui.createMenu('IHS Functions')
      .addItem('Update Payments', 'updatePayment')
      .addToUi();
}

function updatePayment() {

  //Payment Data tab variables
  const paymentDataSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Payment Data");
  const paymentData = paymentDataSheet.getRange("B7:O1000").getValues();

  //PAYMENT tab variables
  const paymentSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("PAYMENT");
  const inputAreaValues = paymentSheet.getRange("B5:L1000").getValues();
  const existID = paymentSheet.getRange("B5:B1000"). getValues();

  //function to remove empty data from any list
  function rmEmpty(list) {
    return list[0] != "";  
  };

  //filter out the empty elements in paymentData array
  let realPaymentData = paymentData.filter(rmEmpty);
  //construct the input data to write to PAYMENT; and the ID list to check if data is already input
  let idList = [];
  let paymentInput = [];
  for (const data of realPaymentData) {
    //refer to Payment Data tab row 5
    const inputFormat = [data[0], data[5], data[6], data[8], data[9], data[7], "Petty Cash", "", data[13], data[1], data[2]];
    paymentInput.push(inputFormat);
    idList.push(data[0]);
  };

  Logger.log("Total Rows of Data: " + paymentInput.length);
  Logger.log(paymentInput);

  //modify paymentInput by removing the already inputed data
  //getting the index of each inputed data
  let realExistID = existID.filter(rmEmpty).flat();
  let indexList = [];
  for (const data of paymentInput) {
    if (realExistID.includes(data[0])) {
      const index = paymentInput.indexOf(data);
      indexList.push(index);
      Logger.log("found " + data[0] + ", index: " + index);
    };
  };

  Logger.log(indexList);

  //removing the inputed data
  for (let i = indexList.length - 1; i>-1; i--) {
    Logger.log("removing " + indexList[i])
    paymentInput.splice(indexList[i], 1);
  }
  
  //get the starting row to write the data
  let inputStartRow;
  let i = 0;
  while (i < inputAreaValues.length) {
    if (inputAreaValues[i][4] == "" && inputAreaValues[i][6] == "") {
      inputStartRow = i + 5;
      break;
    };

    i++;
  };

  //constructing the range for the final input
  inputStartRow.toString();
  const inputEndRow = paymentInput.length + inputStartRow - 1;
  inputEndRow.toString();
  const finalInputRangeA1Notation = "B" + inputStartRow + ":L" + inputEndRow;
  const finalInputRange = paymentSheet.getRange(finalInputRangeA1Notation);

  Logger.log(paymentInput);
  Logger.log(finalInputRangeA1Notation);

  if (paymentInput != "") {
    finalInputRange.setValues(paymentInput);
    const msg = paymentInput.length.toString() + " row of data is added at " + finalInputRangeA1Notation;
    SpreadsheetApp.getUi().alert(msg);
  } else {
    const msg = "There is no update on the payments!"
    SpreadsheetApp.getUi().alert(msg);
  };
  
};
