let categoriesNames = [];
let categoriesValues = [];
let categoriesColors = [];

fetch("/manager/user_categories")
    .then(response => response.json())
    .then(data => {
        categoriesNames = data.map(item => item.category_name);
        categoriesValues = data.map(item => item.category_all_expenses);
        categoriesColors = data.map(item => item.category_color);
        
        criaGrafico()
    })
    
function criaGrafico() {
    const canvas = document.getElementById('chart')
    const ctx = canvas.getContext('2d');

    // Cria o gráfico de pizza
    const expensesChart = new Chart(ctx, {
        type: 'pie', // Tipo de gráfico
        data: {
            labels: categoriesNames, // Labels das fatias
            datasets: [{ 
                label: 'Gasto em reais',
                data: categoriesValues, // Dados para cada categoria
                backgroundColor: categoriesColors,
                borderColor: categoriesColors,
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
