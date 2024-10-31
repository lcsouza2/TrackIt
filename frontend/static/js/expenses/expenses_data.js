let expenseTypes = []
let expenseDate = {"init": "", "end" : ""}
let expenseCategories = [];
let expenseValues = {"init": "", "end": ""}


let expenseTypeFilters = document.querySelectorAll("#expense-type input[type='checkbox']");
let expenseDateInit = document.getElementById("date-start");
let expenseDateEnd = document.getElementById("date-end");
let expenseCategoriesFilters = document.querySelectorAll("canvas");
let expenseValueInit = document.getElementById("value-start");
let expenseValueEnd = document.getElementById("value-end");


function getCanvasColor(canvas) {
    let canvasColor = window.getComputedStyle(canvas).backgroundColor

    return canvasColor !== "rgb(108, 117, 125)"
}

let filters = document.getElementById("filters-form")

filtersForm.addEventListener("change", function(){

    expenseTypes = [];
    expenseDate = {"init": expenseDateInit.value, "end" : expenseDateEnd.value};
    expenseCategories = [];
    expenseValues = {"init": expenseValueInit.value, "end": expenseValueEnd.value};

    expenseTypeFilters.forEach(element => {
        if (element.checked) {
            expenseTypes.push(element.id);
        }
    });

    document.querySelectorAll(".expense-category canvas").forEach(element => {
        if (getCanvasColor(element)) {
            expenseCategories.push(element.id);
            console.log(expenseCategories)
        }
    })
})





fetch("/manager/expenses/get_expenses", {
    method: "POST",
    headers: {
        "Content-Type": "apllication/json"
    },
    body: {
        types: []
    }
})
    
    .then(response => response.json())
    .then(data => function(){
        for (let i in data) {
            console.log(i)
        }
    })

