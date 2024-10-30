let filtersForm = document.getElementById("filters-form")
filtersForm.addEventListener("change", function(event){
    event.preventDefault();
    filtersForm.querySelectorAll("*").forEach(element => {
        console.log(element.value)
    })

})

fetch("/expenses/get_expenses")
    .then(response => response.json())
    .then(data => )

