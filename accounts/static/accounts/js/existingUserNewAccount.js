document.addEventListener('DOMContentLoaded', () =>{
  document.querySelector('.submit').onclick = () =>{
    const userId = document.querySelector("#select").value;
    const amount = document.querySelector("#amount").value;
    const date = document.querySelector("#date").value;
    let type = "single";
    if(document.querySelector('#single').checked == false){
       type = "multiple";
    }
    if(userId == "0" || amount ==""){
      window.alert("Entered Invalid User or Amount !!!");
      return false;

    }
    const request  = new XMLHttpRequest();
    request.open('POST', '/user/newAccount/existing/form');

    request.onload = () =>{
      const data = JSON.parse(request.responseText);
      if(data.status == "closed"){
        const message = `New account opened name : ${data.firstName}, amount : ${amount} on date ${data.date}.`;
        document.querySelector('#result').innerHTML = message;
      }
      else if(data.status == "open"){
        window.alert("Close the account or create a new user 2 !!!");
        return false;
      }

      // Resetting values.
        document.querySelector("#select").value ="0";
        document.querySelector("#amount").value = "";
        document.querySelector('#single').checked = true;
    }

    const info = new FormData();
    info.append('userObj', userId);
    info.append('amount', amount);
    info.append('type', type);
    info.append('date', date)
    request.send(info);

    return false;

  }
});
