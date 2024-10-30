fetch("/manager/user_manager_data")
    .then(response => response.json())
    .then(data => {
        for (let key in data) {
            if (data[key] === null) {
                data[key] = 0;
            }
        }
        
        if (data.this_week > 150) {
            document.getElementById("week-expenses").textContent = `Gasto dessa semana: R$${data.this_week} vamos pisar no freio?`
        } else {
            document.getElementById("week-expenses").textContent = `Gasto dessa semana: R$${data.this_week} ta de boa ainda!`
        }
        
        document.getElementById("today-expenses").textContent = `Gasto de hoje: R$${data.today}`
        document.getElementById("this-month-expenses").textContent = `Gasto desse mês: R$${data.this_month}`
        document.getElementById("more-expensive-category").textContent = `Categoria com maior gasto: ${data.biggest_category}`
        
        document.getElementById("all-installments").textContent = `Parcelamentos ativos: ${data.installments}`

    });