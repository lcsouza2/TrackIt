let loginForm = document.getElementById("login_form");
let loginEmail = document.getElementById("login_email");
let loginPassword = document.getElementById("login_password");
let loginStayLogged = document.getElementById("stay_logged");

loginForm.addEventListener("submit", function(event) {
    event.preventDefault();
    
    const stayLogged = loginStayLogged.checked;

    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
                "email": loginEmail.value,
                "password": loginPassword.value,
                "stay_logged": stayLogged,
            })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => {
                    alert("Erro: " + error.detail);
                    console.error("Erro:", error.detail);
                })
            } else {
                window.location.href=("/manager");
            }
        })
        .catch(error => {
            alert("Erro:", error);
        })
    })

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
    }

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
            return response.json().then(error => {
               console.error("Erro:", error.detail);
               alert("Erro: " + error.detail);
            })
        } else {
            alert("Registrado com sucesso, vamos te redirecionar");
            window.location.href = "/manager";
            sessionStorage.setItem("sessionToken", data.Session_JWT);
        }
    })
        
    })
    .catch((error) => {
        console.error('Error:', error);
    });

