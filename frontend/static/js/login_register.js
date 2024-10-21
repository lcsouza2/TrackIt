let loginForm = document.getElementById("login_form");
let loginUsername = document.getElementById("login_username");
let loginPwd = document.getElementById("login_pwd");

 
//=====================================================================
let registerForm = document.getElementById("form_register");
let registerUsername = document.getElementById("register_username");
let registerEmail = document.getElementById("register_email");
let registerPwd = document.getElementById("register_pwd");
let registerPwdConfirm = document.getElementById("register_pwd_confirm");


registerForm.addEventListener("submit", function(event) {
    event.preventDefault();

    if (registerPwd.value != registerPwdConfirm.value) {
        document.getElementById("no_match_pwd").style = "display: flex;";
        return null;
    } else {
        document.getElementById("no_match_pwd").style = "display: none;";
    };


    fetch("/register_user", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "username": registerUsername.value, 
            "email": registerEmail.value, 
            "password": registerPwd.value
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.Status === "User Already Exists")
        alert('O Email já está sendo usado!');
        throw new Error("Usuário já existe")
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
