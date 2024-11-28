let formCreateExpense = document.getElementById("form-create-expense")
let descriptionNormalExpense = document.getElementById("add-expense-description")
let valueNormalExpense = document.getElementById("add-expense-value")
let dateNormalExpense = document.getElementById("add-expense-date")
let categoryvalueNormalExpense = document.getElementById("add-expense-category")

let categoryNormalExpense = document.querySelector("#add-expense-category")
let categoryColorStyle = window.getComputedStyle(categoryNormalExpense).getPropertyValue("color")


formCreateExpense.addEventListener("submit", function (event) {
    event.preventDefault()

    console.log(categoryColorStyle)

    if (document.getElementById("add-expense-type").value == "Comum") {
        fetch("/manager/register_expense", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                "description"     : descriptionNormalExpense.value,
                "value"           : valueNormalExpense.value,
                "date"            : dateNormalExpense.value,
                "category"        : categoryNormalExpense.value,
                "category_color"  : categoryColorStyle
            })
        })
    .then(function (response) {
        response.json()
        console.log(response)
    })
    .catch(function (error) {
        console.error(error)
    })
    }
})