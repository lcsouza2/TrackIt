export function openPopup(popupId) {
    document.getElementById(popupId).style.display = 'flex'; // Exibe o pop-up
}

// Função para fechar o pop-up
export function closePopup(popupId) {
    document.getElementById(popupId).style.display = 'none'; // Esconde o pop-up
    document.getElementById(popupId).style.animation = ''; // Esconde o pop-up
}
