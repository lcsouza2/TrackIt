let buttonStatus = false;
let buttonMenu = document.getElementById("menu-expand")
let menuOptions = document.getElementById("options")

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

let expenseType = document.getElementById("add-expense-type")
let otherFields = document.getElementById("add-expense-other-fields")

expenseType.addEventListener("change", function(){
    if (expenseType.value === "Comum") {

        otherFields.classList.remove('parcelamento-expanded');

        setTimeout(() => {
            otherFields.classList.add('comum-expanded')
            otherFields.innerHTML = `
                <label for="add-expense-description"></label>
                <input type="text" id="add-expense-description" placeholder="Dê uma breve descrição sobre a despesa" required>
                
                <input type="number" id="add-expense-value" placeholder="Digite o o valor da despesa" required>
                
                <label for="add-expense-date">Selecione a data da despesa</label>
                <input type="date" id="add-expense-date" required>
                
                <label for="category">Selecione a categoria da despesa</label>
                <select name="category" id="add-expense-category">
                    <option value="home-bills" style="color: #ff595e;">Contas da casa</option>
                    <option value="food" style="color: #ffca3a;">Comida</option>
                    <option value="health" style="color: #8ac926;">Saúde</option>
                    <option value="taxes" style="color: #1982c4;">Impostos</option>
                    <option value="new" style="color: #6a4c93;">Nova categoria</option>
                </select>
            `
        }, 200);
        
        
    } else {

        
        otherFields.classList.remove('comum-expanded');
        setTimeout(() => {
            document.getElementById("add-expense-other-fields").innerHTML = ``
            otherFields.classList.add('parcelamento-expanded');
            document.getElementById("add-expense-other-fields").innerHTML = 
            ` 
                <input type="text" id="add-expense-description" placeholder="Dê uma breve descrição sobre a despesa" required>        
                <input type="number" id="add-expense-installment-value" placeholder="Digite o valor de cada parcela" required>
                <input type="number" id="add-expense-installments" placeholder="Digite a quantidade de parcelas" required>
                <input type="number" id="add-expense-interests" placeholder="Digite a porcentagem de juros" required>
                
                <label for="add-expense-date">Informe a data de início</label>
                <input type="date" id="add-expense-date" required>

                <label for="category">Selecione a categoria do parcelamento</label>
                <select name="category" id="add-installment-category">
                    <option value="home-bills" style="color: #ff595e;">Contas da casa</option>
                    <option value="food" style="color: #ffca3a;">Comida</option>
                    <option value="health" style="color: #8ac926;">Saúde</option>
                    <option value="taxes" style="color: #1982c4;">Impostos</option>
                    <option value="new" style="color: #6a4c93;">Nova categoria</option>
                </select>
            `
        }, 200);


    }
}
)


buttonMenu.addEventListener("click", function(){
    if (buttonStatus !== true) {
        buttonStatus = true

        menuOptions.animate([
            {width: "70px", visibility:"hidden"},
            {width: "650px", visibility:"visible"},
        ],
            {
                duration: 500,
                fill: "forwards"
            }
        
        );

        buttonMenu.animate(
            [
                { transform: 'rotate(0deg)', backgroundColor: '#FFFFFF', color: '#4050FC'}, // Estado inicial
                { transform: 'rotate(180deg)', backgroundColor: '#4050FC', color: '#FFFFFF'} // Estado final
            ],
            {
            fill: 'forwards',
            duration: 400, // Duração da animação em milissegundos (1 segundo)
            iterations: 1 
            }
        )

    } else {
        buttonStatus = false

        menuOptions.animate([
            {width: "650px", visibility:"visible"},
            {width: "70px", visibility:"hidden"}
        ],
            {
                duration: 500,
                fill: "forwards"
            }
        
        );

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



function criaGrafico() {
    const canvas = document.getElementById('chart')
    const ctx = canvas.getContext('2d');

    // Cria o gráfico de pizza
    const enpensesChart = new Chart(ctx, {
        type: 'pie', // Tipo de gráfico
        data: {
            labels: ['Categoria 1', 'Categoria 2', 'Categoria 3'], // Labels das fatias
            datasets: [{ 
                label: 'Despesas',
                data: [30, 50, 20], // Dados para cada categoria
                backgroundColor: [ // Cores das fatias
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)'
                ],
                borderColor: [ // Cores das bordas
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                borderWidth: 1 // Espessura da borda
            }]
        },
        options: {
            responsive: true, // Gráfico responsivo
            plugins: {
                legend: {
                    display: true,
                    position: 'right', // Posição da legenda
                    labels: {  
                        boxWidth: 50,
                        padding: 40,
                        font: {
                            size: 15,
                        }
                    }
                }
            },
            animation: {
                animateScale: true, // Animação de escala
                animateRotate: true // Animação de rotação
            }
        }
    });
}

// Chama a função para criar o gráfico quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', criaGrafico);