import { openPopup, closePopup } from "../utils.js";

// Abrir pop-up "Sobre Nós"
document.getElementById('about_us').addEventListener('click', function() {
    openPopup('popup_about_us');
});

// Abrir pop-up "Sobre o TrackIt"
document.getElementById('about_trackit').addEventListener('click', function() {
    openPopup('popup_about_trackit');
});

document.getElementById("login").addEventListener("click", function(){
    openPopup("popup_login");
});

document.getElementById("register").addEventListener("click", function(){
    openPopup("popup_register");
});

// Fechar pop-up ao clicar no 'X'
document.querySelectorAll('.close').forEach(function(closeButton) {
    closeButton.addEventListener('click', function() {
        closePopup(this.closest('.popup').id);
    });
});
