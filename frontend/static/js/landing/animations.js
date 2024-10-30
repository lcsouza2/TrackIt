// Função para abrir o pop-up
function openPopup(popupId) {
    document.querySelector('.content').classList.add('blur'); // Aplica desfoque ao fundo
    document.getElementById(popupId).style.display = 'flex'; // Exibe o pop-up
}

// Função para fechar o pop-up
function closePopup(popupId) {
    document.querySelector('.content').classList.remove('blur'); // Remove o desfoque
    document.getElementById(popupId).style.display = 'none'; // Esconde o pop-up
    document.getElementById(popupId).style.animation = ''; // Esconde o pop-up
}

// Abrir pop-up "Sobre Nós"
document.getElementById('about_us').addEventListener('click', function() {
    openPopup('popup_about_us');
});

// Abrir pop-up "Sobre o TrackIt"
document.getElementById('about_trackit').addEventListener('click', function() {
    openPopup('popup_about_trackit');
});

// Fechar pop-up ao clicar no 'X'
document.querySelectorAll('.close').forEach(function(closeButton) {
    closeButton.addEventListener('click', function() {
        closePopup(this.closest('.popup').id);
    });
});


document.getElementById("login").addEventListener("click", function(){
    openPopup("popup_login");
});

document.getElementById("register").addEventListener("click", function(){
    openPopup("popup_register");
});

