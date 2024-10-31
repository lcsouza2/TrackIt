let filtersStatus = true;
let retractFilters = document.getElementById("retract-filters");
let tablesDiv = document.getElementById("tables");
let filtersForm = document.getElementById("filters-form");

retractFilters.addEventListener("click", function(){
    if (filtersStatus === true) {
        filtersStatus = false;
       
        filtersForm.style.width = "40px"
        filtersForm.style.textWrap = "nowrap"

        tablesDiv.style.width = "98%"
        tablesDiv.style.marginLeft = "2%"
    } else {
        filtersStatus = true;

        filtersForm.style.width = "20%"
        setTimeout(function(){
            filtersForm.style.textWrap = "wrap"
        }, 1000)

        tablesDiv.style.width = "80%"
        tablesDiv.style.marginLeft = "20%"
    }
})

let categoriesDetails = document.getElementById("expense-categories");

fetch("/manager/user_categories")
    .then(response => response.json())
    .then(data => {
        for (let i in data) {

            let div = document.createElement("div")
            div.className = "expense-category"

            let canvas = document.createElement("canvas");
            canvas.style.backgroundColor = data[i].category_color;
            canvas.id = data[i].category_name;
            let canvasState = true;

            canvas.addEventListener("click", () => {

                if (canvasState) {
                    canvasState = false;
                    canvas.animate([
                        {backgroundColor: data[i].category_color},
                        {backgroundColor: "#6c757d"}
                    ],
                    {
                        duration: 300,
                        fill: "forwards"
                    }
                )

                label.animate([
                    {color: "#9676F1", textDecoration: "none"},
                    {color: "#6c757d", textDecoration: "line-through"}

                    ],
                    {
                        duration: 300,
                        fill: "forwards"
                    }
                )
                } else {
                    canvasState = true;
                    canvas.animate([
                        {backgroundColor: "#6c757d"},
                        {backgroundColor: data[i].category_color}
                    ],
                    {
                        duration: 300,
                        fill: "forwards"
                    }
                )
                label.animate([
                    {color: "#6c757d", textDecoration: "line-through"},
                    {color: "#9676F1", textDecoration: "none"}

                    ],
                    {
                        duration: 300,
                        fill: "forwards"
                    }
                )
                }
                const event = new Event("change", {bubbles: true});
                filtersForm.dispatchEvent(event)
            })

            div.appendChild(canvas);
            

            let label = document.createElement("label");
            label.htmlFor = canvas
            label.textContent = data[i].category_name
            div.appendChild(label);

            categoriesDetails.appendChild(div)

        }
        
    }
    )
