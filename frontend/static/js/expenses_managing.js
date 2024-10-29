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

{/* <input type="text" id="add-expense-description" placeholder="Dê uma breve descrição sobre a despesa" required>        
<input type="number" id="add-installment-value" placeholder="Digite o valor de cada parcela" required>
<input type="number" id="add-installments" placeholder="Digite a quantidade de parcelas" required>
<input type="number" id="add-interests" placeholder="Digite a porcentagem de juros" required>

<label for="add-start-date">Informe a data de início</label>
<input type="date" id="add-start-date" required>

<label for="category">Selecione a categoria do parcelamento</label>
<select name="category" id="add-installment-category">
    <option value="new-category" style="color: #6a4c93;">Nova categoria</option>
</select>
<button type="submit">Feito!</button> */}


let installmentValue = document.getElementById("add-installment-value")
let installmentsQuantity = document.getElementById("add-installments")

formCreateExpense.addEventListener("submit", function(event){
    event.preventDefault();

    if (expenseCategory.value === "new-category") {
        openPopup(popup-add-category);
        formCreateCategory.addEventListener("submit", function(event) {
            fetch("/manager/create_ctaegory", {
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
                    fetch("/manager/register_expense", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            "description": expenseDescription.value,
                            "value": expenseValue.value,
                            "date": expenseDate.value,
                            "category" : nameNewCategory
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
                }
            })
        })

    } else {
        fetch("/manager/register_expense", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "description": expenseDescription.value,
                "value": expenseValue.value,
                "date": expenseDate.value,
                "category" : expenseCategory.value
            })
        })
        .then(response => {
            if (response.ok) {
                alert("Nova despesa criada!")
                location.reload()
            }  else if (response.status === 409) {
                alert("A despesa já existe!")
                return
            }
        })
        .catch(error => {
            console.error(error);
        })
    }
})
