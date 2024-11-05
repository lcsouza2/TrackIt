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

let formCreateCategory = document.getElementById("new-category-form")
let nameNewCategory = document.getElementById("new-category-name")
let colorNewCategory = document.getElementById("new-category-color")


let formCreateExpense = document.getElementById("form-create-expense")

let expenseDescription = document.getElementById("add-expense-description")

let expenseValue = document.getElementById("add-expense-value")
let expenseDate = document.getElementById("add-expense-date")


let installmentInterests = 

function createExpense(category) {
    fetch("/manager/register_expense", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "description": expenseDescription.value,
            "value": expenseValue.value,
            "date": expenseDate.value,
            "category" : category
        })
    })
    .then(response => {
        if (response.ok) {
            alert("Nova despesa criada!")
            location.reload()
        }  
    })
    .catch(error => {
        if (error.status === 401) {
            alert("A categoria já existe")
            return
        }
    })
}

function createInstallment(category) {
    fetch("/manager/register_installment", {
        method: "POST",
        headers: {
            "Content-Type" : "application/json"
        },
        body: JSON.stringify({
            "description"       : document.getElementById("add-expense-description").value,
            "category"          : category,
            "quantity"          : document.getElementById("add-installments").value,
            "installment_value" : document.getElementById("add-installment-value").value,
            "init_date"         : document.getElementById("add-start-date").value,
            "interests"         : document.getElementById("add-interests").value
        })
    })
    .then( response => {

        if (response.ok) {
            alert("Parcelamento criado!")
        }
    })
}

function createCategory() {
    fetch("/manager/create_category", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "name" : nameNewCategory.value,
            "color" : colorNewCategory.value
        })
    })
}

formCreateExpense.addEventListener("submit", function(event){
    event.preventDefault();

    let expenseCategory = document.getElementById("add-category")

    const expenseType = document.getElementById("add-expense-type").value;

    if (expenseCategory.value === "new-category") {
        // Abre o popup para criar nova categoria
        openPopup("popup-add-category");

        // Adiciona listener ao formulário de criação de categoria uma única vez
        formCreateCategory.addEventListener("submit", function(event) {
            event.preventDefault();
            createCategory().then(response => {
                if (response.ok) {
                    alert("Nova categoria criada com sucesso!");
                    closePopup("popup-add-category");

                    // Depois de criar a nova categoria, registra a despesa ou parcelamento
                    if (expenseType === "Comum") {
                        createExpense(nameNewCategory.value);
                    } else {
                        createInstallment(nameNewCategory.value);
                    }
                }
            });
        }, { once: true });

    } else {
        // Registrar despesa ou parcelamento com categoria existente
        if (expenseType === "Comum") {
            createExpense(expenseCategory.value);
        } else {
            createInstallment(expenseCategory.value);
        }
    }
});
