fetch("/manager/user_manager_data")
    .then(response => response.json())
    .then(data => {

       if (data.this_week > 150) {
            document.getElementById("week-expenses").textContent = `Gasto dessa semana: R$${data.this_week} vamos pisar no freio?`
        } else {
            document.getElementById("week-expenses").textContent = `Gasto dessa semana: R$${data.this_week} ta de boa ainda!`
        }
    })