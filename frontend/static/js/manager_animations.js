let buttonStatus = false;
let buttonMenu = document.getElementById("menu-expand")
let menuOptions = document.getElementById("options")


buttonMenu.addEventListener("click", function(){
    if (buttonStatus !== true) {
        buttonStatus = true

        menuOptions.animate([
            {width: "70px", visibility:"hidden"},
            {width: "650px", visibility:"visible"}
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
    const meuGraficoPizza = new Chart(ctx, {
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