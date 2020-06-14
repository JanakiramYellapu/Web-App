document.addEventListener('DOMContentLoaded', () =>{
  document.querySelector('.submit').onclick = () =>{
    const firstName = document.querySelector("#firstName").value;
    const lastName = document.querySelector("#lastName").value;
    const mobileNo = document.querySelector("#mobileNo").value;
    const amount = document.querySelector("#amount").value;
    const date = document.querySelector("#date").value;
    if(firstName == "" || amount =="" || amount == "0" || date == ""){
      window.alert("Entered Invalid User or Amount !!!");
      return false;

    }
    const request  = new XMLHttpRequest();
    request.open('POST', '/accounts/user/newAccount/new/form');

    request.onload = () =>{
        const data = JSON.parse(request.responseText);
        const message = `New account opened Name : ${data.firstName}, Amount : ${data.amount}.`;
        document.querySelector('#result').innerHTML = message;

        // Resetting values.
        document.querySelector('#firstName').value = "";
        document.querySelector('#lastName').value = "";
        document.querySelector('#mobileNo').value = "";
        document.querySelector('#amount').value = "";

    }

    const info = new FormData();
    info.append('firstName', firstName);
    info.append('lastName', lastName);
    info.append('mobileNo', mobileNo);
    info.append('amount', amount);
    info.append('date', date);
    request.send(info);

    return false;

  }
});
