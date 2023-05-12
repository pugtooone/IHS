/** @OnlyCurrentDoc */
function onOpen(e) {

  autoUpdateBrand();
  autoUpdatePayment();
  autoUpdateModel();

  SpreadsheetApp.flush();

  //Brand Name

  function autoUpdateBrand() {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const brandName = ss.getName().split("_")[1];
    const brandCell = ss.getSheetByName("Payment & Model Booking Data").getRange('C2');

    if (brandCell.getValue !== brandName) {
      brandCell.setValue(brandName);
      Logger.log("Brand name has been updated.")
    } else {
      Logger.log("Brand name is correct.")
    };
  };

  //function to remove empty data from any list
  function rmEmpty(list) {
    return list[0] != "";  
  };

  //Payment

  function autoUpdatePayment() {
    //Payment Data tab variables
    const paymentDataSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Payment & Model Booking Data");
    const paymentData = paymentDataSheet.getRange("B7:O1000").getValues();

    //PAYMENT tab variables
    const paymentSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("PAYMENT");
    const paymentInputAreaValues = paymentSheet.getRange("B5:L1000").getValues();
    const paymentExistID = paymentSheet.getRange("B5:B1000"). getValues();

    //filter out the empty elements in paymentData array
    let realPaymentData = paymentData.filter(rmEmpty);
    //construct the input data to write to PAYMENT; and the ID list to check if data is already input
    let paymentIDList = [];
    let paymentInput = [];
    for (const data of realPaymentData) {
      //refer to Payment Data tab row 5
      const inputFormat = [data[0], data[5], data[6], data[8], data[9], data[7], "Petty Cash", "", data[13], data[1], data[2]];
      paymentInput.push(inputFormat);
      paymentIDList.push(data[0]);
    };

    if (paymentInput != "") {
      Logger.log("Total Rows of Payment Data: " + paymentInput.length);
      Logger.log("Payment Data: " + paymentInput);
    } else {
      Logger.log("No payment data");
      const msg = "There is no update on the payments!";
      SpreadsheetApp.getUi().alert(msg);
      return 0;
    };

    //modify paymentInput by removing the already inputed data
    //getting the index of each inputed data
    let realPaymentExistID = paymentExistID.filter(rmEmpty).flat();
    let existPaymentIndexList = [];
    let existPaymentIDList = [];
    for (const data of paymentInput) {
      if (realPaymentExistID.includes(data[0])) {
        const index = paymentInput.indexOf(data);
        existPaymentIndexList.push(index);
        existPaymentIDList.push(data[0]);
        Logger.log("Found Exiting ID:" + data[0] + " - Index: " + index);
      };
    };

    if (existPaymentIndexList != "") {
      Logger.log("List of Existing payment ID: " + existPaymentIDList);
    };

    //removing the inputed data
    for (let i = existPaymentIndexList.length - 1; i>-1; i--) {
      Logger.log("Removing ID[" + existPaymentIDList[i] + "] from the payment ID List")
      paymentInput.splice(existPaymentIndexList[i], 1);
    }
    
    //get the starting row to write the data
    let paymentInputStartRow;
    let i = 0;
    while (i < paymentInputAreaValues.length) {
      //check if Invoiced Amount and Payment Methods have input
      if (paymentInputAreaValues[i][4] == "" && paymentInputAreaValues[i][6] == "") {
        paymentInputStartRow = i + 5;
        break;
      };

      i++;
    };

    //constructing the range for the final input
    paymentInputStartRow.toString();
    const paymentInputEndRow = paymentInput.length + paymentInputStartRow - 1;
    paymentInputEndRow.toString();
    const finalPaymentInputRangeA1Notation = "B" + paymentInputStartRow + ":L" + paymentInputEndRow;
    const finalPaymentInputRange = paymentSheet.getRange(finalPaymentInputRangeA1Notation);

    if (paymentInput != "") {
      Logger.log("Final Payment Input: " + paymentInput);
      Logger.log("Final Payment Input Range: " + finalPaymentInputRangeA1Notation);
      finalPaymentInputRange.setValues(paymentInput);
      const msg = paymentInput.length.toString() + " row of data is added at " + finalPaymentInputRangeA1Notation;
      SpreadsheetApp.getUi().alert(msg);
    } else {
      Logger.log("No update on payment")
      const msg = "There is no update on the payments!"
      SpreadsheetApp.getUi().alert(msg);
    };
  };

  //Model Booking

  function autoUpdateModel() {
    //Model booking data tab variables
    const bookingDataSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Payment & Model Booking Data");
    const bookingData = bookingDataSheet.getRange("Q7:AK1000").getValues();

    //MODEL BOOKING tab variables
    const bookingSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("MODEL BOOKING");
    const bookingInputAreaValues = bookingSheet.getRange("B5:R1000").getValues();
    const bookingExistID = bookingSheet.getRange("B5:B1000"). getValues();

    //filter out the empty elements in bookingData array
    let realBookingData = bookingData.filter(rmEmpty);
    //construct the input data to write to MODEL BOOKING; and the ID list to check if data is already input
    let bookingIDList = [];
    let bookingInput = [];
    for (const data of realBookingData) {
      //existing data with "NA" ID will not be recorded
      if (data[0] !== "NA") {
        //refer to Data tab row 5
        const inputFormat = [data[0], data[4], data[2], data[6], data[18], data[19], data[1], data[17], data[9], data[10], data[11], data[12], data[13], data[14], data[15], data[16], data[20]];
        bookingInput.push(inputFormat);
        bookingIDList.push(data[0]);
      };
    };

    if (bookingInput != "") {
      Logger.log("Total Rows of Model Booking Data: " + bookingInput.length);
      Logger.log("Model Booking Data: " + bookingInput);
    } else {
      Logger.log("No Model Data");
      const msg = "There is no update on model bookings!";
      SpreadsheetApp.getUi().alert(msg);
      return 0;
    };

    //modify bookingInput by removing the already input data
    //getting the index of each already input data
    let realBookingExistID = bookingExistID.filter(rmEmpty).flat();
    let existBookingIndexList = [];
    let existBookingIDList = [];
    for (const data of bookingInput) {
      if (realBookingExistID.includes(data[0])) {
        const index = bookingInput.indexOf(data);
        existBookingIndexList.push(index);
        existBookingIDList.push(data[0]);
        Logger.log("Found Exiting ID: " + data[0] + " - Index: " + index);
      };
    };

    if (existBookingIndexList != "") {
      Logger.log("List of Existing model booking ID: " + existBookingIDList);
    };

    //removing the already input data from the bookingInput (start from the end as starting from the beginning will shift the index)
    for (let i = existBookingIndexList.length - 1; i>-1; i--) {
      Logger.log("Removing ID[" + existBookingIDList[i] + "] from the Model ID List");
      bookingInput.splice(existBookingIndexList[i], 1);
    }
    
    //get the starting row to write the data
    let bookingInputStartRow;
    i = 0;
    while (i < bookingInputAreaValues.length) {
      //check if the Talent name and Booking Date have input
      if (bookingInputAreaValues[i][2] == "" && bookingInputAreaValues[i][8] == "") {
        bookingInputStartRow = i + 5;
        break;
      };

      i++;
    };

    //constructing the range for the final input
    bookingInputStartRow.toString();
    const bookingInputEndRow = bookingInput.length + bookingInputStartRow - 1;
    bookingInputEndRow.toString();
    const finalBookingInputRangeA1Notation = "B" + bookingInputStartRow + ":R" + bookingInputEndRow;
    const finalBookingInputRange = bookingSheet.getRange(finalBookingInputRangeA1Notation);

    if (bookingInput != "") {
      Logger.log("Final Model Booking Input: " + bookingInput);
      Logger.log("Final Model Booking Input Range: " + finalBookingInputRangeA1Notation);
      finalBookingInputRange.setValues(bookingInput);
      const msg = bookingInput.length.toString() + " row of data is added at " + finalBookingInputRangeA1Notation;
      SpreadsheetApp.getUi().alert(msg);
    } else {
      Logger.log("No update on model booking")
      const msg = "There is no update on model bookings!";
      SpreadsheetApp.getUi().alert(msg);
    };
  };

};
