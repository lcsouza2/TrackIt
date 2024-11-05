
function openPopup(id) {
    document.querySelector(".popup").classList.add('blur');
    document.getElementById(id).style.display = "flex";
}

function closePopup(id) {
    document.querySelector(".popup").classList.remove("blur");
    document.getElementById(id).style.display = 'none';
    document.getElementById(id).style.animation = '';
}

document.querySelectorAll('.close').forEach(function(closeButton) {
    closeButton.addEventListener('click', function() {
        closePopup(this.closest('.popup').id);
    });
});

document.getElementById("add-expense").addEventListener("click", function(){
    openPopup("create-expense");
})

document.getElementById("see-expenses").addEventListener("click", function(){
    location.href = "/manager/expenses"
})

let expenseType = document.getElementById("add-expense-type")
let otherFields = document.getElementById("add-expense-other-fields")

expenseType.addEventListener("change", function() {
    if (expenseType.value === "Comum") {

        otherFields.style.height = "0px"
        
        setTimeout(() => {
            otherFields.style.height = "260px"
            otherFields.innerHTML = `
                <label for="add-expense-description"></label>
                <input type="text" id="add-expense-description" placeholder="Dê uma breve descrição sobre a despesa" required>
                
                <input type="number" id="add-expense-value" placeholder="Digite o valor da despesa" required>
                
                <label for="add-expense-date">Selecione a data da despesa</label>
                <input type="date" id="add-expense-date" required>
                
                <label for="category">Selecione a categoria da despesa</label>
                <select name="category" id="add-category">
                    <option value="new-category" style="color: #6a4c93;">Nova categoria</option>
                </select>
                <button type="submit">Feito!</button>
            `;

            fetch("/manager/user_categories")
                .then(response => response.json())
                .then(data => {
                    const categorySelect = document.getElementById('add-category');

                    data.forEach(item => {
                        const option = document.createElement('option');
                        option.value = item.category_name;
                        option.textContent = item.category_name;
                        option.style.color = item.category_color;
                        categorySelect.appendChild(option);
                    });
                })
                .catch(error => console.error('Erro:', error));
        }, 200);

    } else {
        otherFields.style.height = "0px";

        setTimeout(() => {
            document.getElementById("add-expense-other-fields").innerHTML = ``;

            otherFields.style.height = "350px";

            document.getElementById("add-expense-other-fields").innerHTML = `
                <input type="text" id="add-expense-description" placeholder="Dê uma breve descrição sobre a despesa" required>        
                <input type="number" id="add-installment-value" placeholder="Digite o valor de cada parcela" required>
                <input type="number" id="add-installments" placeholder="Digite a quantidade de parcelas" required>
                <input type="number" id="add-interests" placeholder="Digite a porcentagem de juros" required>

                <label for="add-start-date">Informe a data de início</label>
                <input type="date" id="add-start-date" required>

                <label for="category">Selecione a categoria do parcelamento</label>
                <select name="category" id="add-category">
                    <option value="new-category" style="color: #6a4c93;">Nova categoria</option>
                </select>
                <button type="submit">Feito!</button>
            `;

            fetch("/manager/user_categories")
                .then(response => response.json())
                .then(data => {
                    const categorySelect = document.getElementById('add-category');

                    data.forEach(item => {
                        const option = document.createElement('option');
                        option.value = item.category_name;
                        option.textContent = item.category_name;
                        option.style.color = item.category_color; 
                        categorySelect.appendChild(option);
                    });
                })
        }, 200);
    }
});

let buttonStatus = false;
let buttonMenu = document.getElementById("menu-expand")
let menuOptions = document.getElementById("options")
buttonMenu.addEventListener("click", function(){
    if (buttonStatus !== true) {
        buttonStatus = true

        menuOptions.style.width = "400px"

        buttonMenu.animate(
            [
                {
                    transform: 'rotate(0deg)', 
                    backgroundColor: '#FFFFFF', 
                    color: '#4050FC'
                }, // Estado inicial
                {
                    transform: 'rotate(180deg)', 
                    backgroundColor: '#4050FC', 
                    color: '#FFFFFF', 
                } // Estado final
            ],
            {
            fill: 'forwards',
            duration: 400, // Duração da animação em milissegundos (1 segundo)
            iterations: 1 
            }
        )

    } else {
        buttonStatus = false

        menuOptions.style.width = "70px"


        buttonMenu.animate(
            [
                {
                    transform: 'rotate(0deg)', 
                    backgroundColor: '#4050FC', 
                    color: '#FFFFFF'
                }, // Estado inicial

                {
                    transform: 'rotate(-180deg)', 
                    backgroundColor: '#FFFFFF', 
                    color: '#4050FC',
                } // Estado final
            ],
            {
            fill: 'forwards',
            duration: 400, // Duração da animação em milissegundos (1 segundo)
            iterations: 1 // Quantas vezes repetir a animação
            }
        )
    }
})

fetch("/manager/user_categories")
    .then(response => response.json())
    .then(data => {
        const categorySelect = document.getElementById('add-category');

        data.forEach(item => {
            const option = document.createElement('option');
            option.value = item.category_name;
            option.textContent = item.category_name;
            option.style.color = item.category_color; 
            categorySelect.appendChild(option);
        });
    })
