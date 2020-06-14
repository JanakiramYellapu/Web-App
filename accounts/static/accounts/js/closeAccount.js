document.addEventListener('DOMContentLoaded', () =>{
  document.querySelector('.submit').onclick = () =>{
    const userId = document.querySelector("#select").value;
    if(userId == "0"){
      window.alert("Entered Invalid User !!!");
      return false;
    }
    const request  = new XMLHttpRequest();
    request.open('POST', '/accounts/user/closeAccount/form');

    request.onload = () =>{
        const data = JSON.parse(request.responseText);
        if(data.status =="success"){
          const message = `Closed account successfully !!!`;
          document.querySelector('#result').innerHTML = message;
        }
        else if(data.status =="failed"){
          const message = `Failed !!!`;
          document.querySelector('#result').innerHTML = message;
        }

        // Resetting values
         document.querySelector("#select").value = "0";
    }
    const info = new FormData();
    info.append('userObj', userId);
    request.send(info);

    return false;

  }
});
