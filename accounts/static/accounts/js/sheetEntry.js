// from http import XMLHttpRequest
// import JSON
// import json
// console.log("hello");
document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('#save').onclick = () =>{
    const request = new XMLHttpRequest();
    const dateId = document.querySelector('#dateId').value;
    const userId = document.querySelector('#userId').value;
    const amount = document.querySelector('#amount').value;
    if(amount == ""  || userId == "0"){
      window.alert("Empty fields!!!");
      return false;
    }
    request.open('POST', '/accounts/sheetEntry/form/data');

    request.onload = ()=>{
          // const data = request.responseText;
          const data = JSON.parse(request.responseText);
          if(data.status == "saved"){
              const message = `The user  ${data.user}  on date  ${data.date}  paid amount  : ${amount}`;
              document.querySelector('#result').innerHTML = message;
          }
          else if (data.status == "updated") {
            const message = `The user  ${data.user}  on date  ${data.date}  updated amount from ${data.prevAmount} to ${amount}`;
            document.querySelector('#result').innerHTML = message;
          }

          // Resetting values
          document.querySelector('#userId').value = "0";
          document.querySelector('#amount').value = "";
    }


    const info = new FormData();
    info.append('date', dateId);
    info.append('userId', userId);
    info.append('amount', amount);
    info.append('action', "Save");
    request.send(info);
    return false;

  }
  document.querySelector('#expenseSave').onclick = () =>{
    const request = new XMLHttpRequest();
    const dateId = document.querySelector('#expDateId').value;
    const expense = document.querySelector('#expId').value;
    const amount = document.querySelector('#expenseAmount').value;
    if(amount == ""  || expense == "0" || amount == "0"){
      window.alert("Empty fields!!!");
      return false;
    }
    request.open('POST', '/accounts/sheetEntry/form/expense');

    request.onload = ()=>{
          const data = JSON.parse(request.responseText);
          if(data.status == "saved"){
              const message = `The ${data.expense}  on date  ${data.date}  expense amount  : ${amount}`;
              document.querySelector('#expenseResult').innerHTML = message;
          }
          else if (data.status == "updated") {
            const message = `The  ${data.expense}  on date  ${data.date}  updated expense amount from ${data.prevAmount} to ${amount}`;
            document.querySelector('#expenseResult').innerHTML = message;
          }
          document.querySelector('#expId').value = "0";
          document.querySelector('#expenseAmount').value ="";
    }


    const info = new FormData();
    info.append('dateId', dateId);
    info.append('expense', expense);
    info.append('amount', amount);
    request.send(info);
    return false;

  }
  document.querySelector('#otherExpenseSave').onclick = () =>{
    const request = new XMLHttpRequest();
    const dateId = document.querySelector('#expDateId').value;
    const expense = document.querySelector('#otherExpenses').value;
    const amount = document.querySelector('#otherExpenseAmount').value;
    if(amount == ""  || expense == "" || amount == "0"){
      window.alert("Empty fields!!!");
      return false;
    }
    request.open('POST', '/accounts/sheetEntry/form/expense');

    request.onload = ()=>{
          const data = JSON.parse(request.responseText);
          if(data.status == "saved"){
              const message = `The ${data.expense}  on date  ${data.date}  expense amount  : ${amount}`;
              document.querySelector('#expenseResult').innerHTML = message;
          }
          else if (data.status == "updated") {
            const message = `The  ${data.expense}  on date  ${data.date}  updated expense amount from ${data.prevAmount} to ${amount}`;
            document.querySelector('#expenseResult').innerHTML = message;
          }
          // Resetting fields
          // document.querySelector('#otherExpenses').value = "";
          // document.querySelector('#otherExpenseAmount').value = "";
    }


    const info = new FormData();
    info.append('dateId', dateId);
    info.append('expense', expense);
    info.append('amount', amount);
    request.send(info);
    return false;

  }
});
