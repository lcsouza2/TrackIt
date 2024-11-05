let expenseTypeFilters = document.querySelectorAll("#expense-type input[type='checkbox']");
let expenseDateInit = document.getElementById("date-start");
let expenseDateEnd = document.getElementById("date-end");
let expenseCategoriesFilters = document.querySelectorAll("canvas");
let expenseValueInit = document.getElementById("value-start");
let expenseValueEnd = document.getElementById("value-end");

let filters = document.getElementById("filters-form")

let editExpenseDiv = document.getElementById("edit-expense")

function updateFiltersAndFetch() {
    let expenseTypes = [];
    let expenseDate = {"init": expenseDateInit.value, "end": expenseDateEnd.value};
    let expenseCategories = [];
    let expenseValues = {"init": expenseValueInit.value, "end": expenseValueEnd.value};

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
        let tableBodyExpenses = document.getElementById("expenses-table").querySelector("tbody");

        let expensesBodyHTML = "";

        for (let i in data.expenses) {
            expensesBodyHTML += `
                        <tr>
                            <td>${data.expenses[i][1]}</td>
                            <td>${data.expenses[i][2]} </td>
                            <td>${data.expenses[i][3]} </td>
                            <td>${data.expenses[i][4]} </td>
                            <td><button class="del-button" id="r ${data.expenses[i][0]}">Excluir</button></td>
                            <td><button class="alt-button" id="e ${data.expenses[i][0]}">Editar</button></td>
                        </tr>
                        `
            }
            tableBodyExpenses.innerHTML = expensesBodyHTML;

            /////////////////////////////
            
            let tableBodyInstallments = document.getElementById("installments-table").querySelector("tbody");
            
            let installmentsBodyHTML = "";

            for (let i in data.installments) {
                installmentsBodyHTML += `
                        <tr>
                            <td>${data.installments[i][1]}</td>
                            <td>${data.installments[i][2]}</td>
                            <td>${data.installments[i][3]}</td>
                            <td>${data.installments[i][4]}</td>
                            <td>${data.installments[i][5]}</td>
                            <td>${data.installments[i][6]}</td>
                            <td><button class="del-button" id="r ${data.installments[i][0]}">Excluir</button></td>
                            <td><button class="alt-button" id="e ${data.installments[i][0]}">Editar</button></td>
                        </tr>
                        `
                }   

            tableBodyInstallments.innerHTML = installmentsBodyHTML;

            let deleteButtons = document.querySelectorAll(".del-button");
            deleteButtons.forEach(element => {
                let spentTypeDel
                if (element.closest("table").id == "expenses-table") {
                    spentTypeDel = "Expense"
                } else {
                    spentTypeDel = "Installment"
                }   
                element.addEventListener("click", () => {
                    if (confirm(`Deseja mesmo excluir a despesa?`)) {
                        handleDeleteAction(spentTypeDel, element.id.split(" ")[1])
                        location.reload()
                    }
                });
            });
        
            let editButtons = document.querySelectorAll(".alt-button");
            editButtons.forEach(element => {
                let spentTypeAlt
                if (element.closest("table").id == "expenses-table") {
                    spentTypeAlt = "Expense"
                } else {
                    spentTypeAlt = "Installment"
                }
                element.addEventListener("click", () =>{
                    handleUpdateAction(spentTypeAlt, element.id)
                });
            });

        })
}

function getCanvasColor(canvas) {
    let canvasColor = window.getComputedStyle(canvas).backgroundColor

    return canvasColor !== "rgb(108, 117, 125)"
}

let debounceTimer;
filtersForm.addEventListener("change", function(){
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(updateFiltersAndFetch, 300)

})

updateFiltersAndFetch()

function handleDeleteAction(spentType, buttonId) {
    fetch("/manager/expenses/delete_expense", {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "type": spentType,
            "id" : buttonId
        })
    })
}

function handleUpdateAction(spentType, buttonId) {    
    document.querySelector(".popup").style.display = "flex"
    let editPopup = document.getElementById("edit-expense")
    editPopup.style.display = "flex";
    
    if (spentType == "Expense") {
        let row = document.getElementById(buttonId).closest("tr")
        
        editPopup.style.height = "260px"
        editPopup.innerHTML = `
            <span class="close">&times;</span>
            <input id="edit-expense-description" type="text", placeholder="Descrição: ${row.cells[0].innerText}">
            <input id="edit-expense-value" type="number" value="${row.cells[1].innerText}" placeholder="Valor: ${row.cells[1].innerText}">
            <input id="edit-expense-date" type="date", value="${row.cells[2].innerText}">
            <select id="edit-category" name="category" >
            </select>
            <button type="submit">Feito</button>
        `

        document.querySelector(".close").addEventListener("click", () => {
            document.querySelector(".popup").style.display = "none";
            document.getElementById("edit-expense").style.display = 'none';
            document.getElementById("edit-expense").style.animation = '';
        })

        fetch("/manager/user_categories")
            .then(response => response.json())
            .then(data => {
                let selectEditPopup = document.getElementById("edit-category")
                for (let i in data) {
                    let option = document.createElement("option")
                    option.value = data[i].category_name
                    option.textContent = data[i].category_name
                    option.style.color = data[i].category_color
                    
                    selectEditPopup.appendChild(option)
                }

            })

        document.getElementById("edit-expense").addEventListener("submit", function(event) {
            event.preventDefault();
            fetch("/manager/expenses/edit_expense", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    "id" : buttonId.split(" ")[1],
                    "description" : document.getElementById("edit-expense-description").value,
                    "value" : document.getElementById("edit-expense-value").value,
                    "date" : document.getElementById("edit-expense-date").value,
                    "category" : document.getElementById("edit-category").value
                }),
            })
            .then(response => {
                if (response.ok) {
                    location.reload()
                }
            })
        })
        
    } else {
        let row = document.getElementById(buttonId).closest("tr")

        editPopup.style.height = "470px"
        editPopup.innerHTML = `
            <span class=close>&times;</span>
            <label for="edit-installment-description">Descrição do Parcelamento</label>
            <input id="edit-installment-description" type="text", value="${row.cells[0].innerText}">

            <label for="edit-installment-value">Valor das Parcelas</label>
            <input id="edit-installment-value" type="number" value="${row.cells[1].innerText}">

            <label for="eit-installment-quantity">Quantidade de Parcelas</label>
            <input id="edit-installment-quantity" type="number", value="${row.cells[2].innerText}">

            <label for="eit-installment-quantity">Taxa de Juros (em %)</label>
            <input id="edit-installment-interests" type="number", value="${row.cells[4].innerText}">

            <label for="edit-installment-description">Data de Início do Parcelamento</label>
            <input id="edit-installment-date" type="date", value="${row.cells[5].innerText}">

            <label for="edit-category"> Categoria</label>
            <select id="edit-category" name="category">
            </select>
            <button type="submit">Feito</button>
        `

        document.querySelector(".close").addEventListener("click", () => {
            document.querySelector(".popup").style.display = "none";
            document.getElementById("edit-expense").style.display = 'none';
            document.getElementById("edit-expense").style.animation = '';
        })

        fetch("/manager/user_categories")
        .then(response => response.json())
        .then(data => {
            let selectEditPopup = document.getElementById("edit-category")
            for (let i in data) {
                let option = document.createElement("option")
                option.value = data[i].category_name
                option.textContent = data[i].category_name
                option.style.color = data[i].category_color
                selectEditPopup.appendChild(option)
                }
        })

        document.getElementById("edit-expense").addEventListener("submit", function(event) {
            event.preventDefault();
            fetch("/manager/expenses/edit_installment", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    "id" : buttonId.split(" ")[1],
                    "description" : document.getElementById("edit-expense-description").value,
                    "value" : document.getElementById("edit-expense-value").value,
                    "date" : document.getElementById("edit-expense-date").value,
                    "category" : document.getElementById("edit-category").value
                }),
            })
            .then(response => {
                if (response.ok) {
                    location.reload()
                }
            })
        })
    }   

}