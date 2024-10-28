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

formCreateCategory.addEventListener("submit", function(event) {
    event.preventDefault();

    fetch("manager/create_category", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "name"  : nameNewCategory.value,
            "color" : colorNewCategory.value
        })
    })
    .then(function(response) {
        if (response.status == 201) {
            fetch("manager/register_expense", {
                method: "POST",
                headers: {
                    "Content-type": "application/json"
                },
                body: JSON.stringify({
                    "description": expenseDescription.value,
                    "value": expenseValue.value,
                    "date": expenseDate.value,
                    "category":nameNewCategory.value,
                }) 
            })
        } else if (response.status == 409){
            alert("A categoria já existe")
        }
    })
})

formCreateExpense.addEventListener("submit", function(event){
    event.preventDefault();

    if(expenseCategory.value == "new-category") {
        openPopup("popup-add-category")
    }
})



