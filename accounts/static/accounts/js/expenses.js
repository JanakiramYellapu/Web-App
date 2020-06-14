document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('#expenseSave').onclick = () =>{
    const request = new XMLHttpRequest();
    const dateId = document.querySelector('#expDateId').value;
    const expense = document.querySelector('#expId').value;
    const amount = document.querySelector('#expenseAmount').value;
    if(amount == ""  || expId == "0" || amount == "0"){
      window.alert("Empty fields!!!");
      return false;
    }
    request.open('POST', '/accounts/sheetEntry/form/expense');

    request.onload = ()=>{
          const data = JSON.parse(request.responseText);
          if(data.status == "saved"){
              const message = `The user  ${data.expense}  on date  ${data.date}  expense amount  : ${amount}`;
              document.querySelector('#expenseResult').innerHTML = message;
          }
          else if (data.status == "updated") {
            const message = `The user  ${data.expense}  on date  ${data.date}  updated expense amount from ${data.prevAmount} to ${amount}`;
            document.querySelector('#result').innerHTML = message;
          }
    }


    const info = new FormData();
    info.append('date', dateId);
    info.append('expense', expense);
    info.append('amount', amount);
    request.send(info);
    return false;

  }
});
