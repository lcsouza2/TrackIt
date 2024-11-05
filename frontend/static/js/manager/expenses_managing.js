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
let expenseCategory = document.getElementById("add-expense-category")


let installmentInterests = document.getElementById("add-interests")
let installmentInitDate = document.getElementById("add-start-date")
let installmentCategory = document.getElementById("add-installment-category")
let installmentValue = document.getElementById("add-installment-value")
let installmentsQuantity = document.getElementById("add-installments")

formCreateExpense.addEventListener("submit", function(event){
    event.preventDefault();

    if (expenseCategory.value === "new-category" || installmentCategory.value === "new-category") {
        openPopup("popup-add-category");
        formCreateCategory.addEventListener("submit", function(event) {
            event.preventDefault();
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
            .then(response => {
                if (response.ok) {
                    if (document.getElementById("add-expense-type").value === "Comum") {

                        fetch("/manager/register_expense", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({
                                "description": expenseDescription.value,
                                "value": expenseValue.value,
                                "date": expenseDate.value,
                                "category" : nameNewCategory.value
                            })
                        })
                        .then(response => {
                            if (response.ok) {
                                alert("Nova categoria e despesa criadas!")
                                location.reload()
                            }  
                        })
                        .catch(error => {
                            if (error.status === 401) {
                                alert("A categoria já existe")
                                return
                            }
                        })
                    } else {
                        fetch("/manager/register_installment", {
                            method: "POST",
                            headers: {
                                "Content-Type" : "application/json"
                            },
                            body: JSON.stringify({
                                "description"       : expenseDescription.value,
                                "category"          : installmentCategory.value,
                                "quantity"          : installmentsQuantity.value,
                                "installment_value" : installmentValue.value,
                                "init_date"         : installmentInitDate.value,
                                "interests"         : installmentInterests.value
                            })
                        })
                    }
                }
            })
        })

    } else {
        if (document.getElementById("add-expense-type").value === "Comum") {

            fetch("/manager/register_expense", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "description": expenseDescription.value,
                    "value": expenseValue.value,
                    "date": expenseDate.value,
                    "category" : nameNewCategory.value
                })
            })
            .then(response => {
                if (response.ok) {
                    alert("Nova categoria e despesa criadas!")
                    location.reload()
                }  
            })
            .catch(error => {
                if (error.status === 401) {
                    alert("A categoria já existe")
                    return
                }
            })
        } else {
            fetch("/manager/register_installment", {
                method: "POST",
                headers: {
                    "Content-Type" : "application/json"
                },
                body: JSON.stringify({
                    "description"       : expenseDescription.value,
                    "category"          : installmentCategory.value,
                    "quantity"          : installmentsQuantity.value,
                    "installment_value" : installmentValue.value,
                    "init_date"         : installmentInitDate.value,
                    "interests"         : installmentInterests.value
                })
            })
            .then(response => {
                if (response.ok) {
                    alert("Novo parcelamento criado ")
                }
            })
        }
    }
})