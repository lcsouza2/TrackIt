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


let filters = document.getElementById("filters-form")


let debounceTimer;

function updateFiltersAndFetch() {
    expenseTypes = [];
    expenseDate = { "init": expenseDateInit.value, "end": expenseDateEnd.value };
    expenseCategories = [];
    expenseValues = { "init": expenseValueInit.value, "end": expenseValueEnd.value };

    expenseTypeFilters.forEach(element => {
        if (element.checked) {
            expenseTypes.push(element.id);
        }
    });

    document.querySelectorAll(".expense-category canvas").forEach(element => {
        if (getCanvasColor(element)) {
            expenseCategories.push(element.id);
        }
    });

    fetch("/manager/expenses/get_expenses", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "expense_types": expenseTypes,
            "expense_date": expenseDate,
            "expense_categories": expenseCategories,
            "expense_values": expenseValues
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => console.error("Error:", error));
}

function getCanvasColor(canvas) {
    let canvasColor = window.getComputedStyle(canvas).backgroundColor

    return canvasColor !== "rgb(108, 117, 125)"
}


filtersForm.addEventListener("change", function(){
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(updateFiltersAndFetch, 300)

})
