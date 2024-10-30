let filtersStatus = true;
let retractFilters = document.getElementById("retract-filters");
let tablesDiv = document.getElementById("tables")
retractFilters.addEventListener("click", function(){
    if (filtersStatus === true) {
        filtersStatus = false;
       
        document.getElementById("filters-form").style.width = "40px"
        tablesDiv.style.width = "98%"
        tablesDiv.style.marginLeft = "2%"
        tablesDiv.querySelectorAll("*").forEach(element => {
            element.style.width = "70%"
        })
    } else {
        filtersStatus = true;
        document.getElementById("filters-form").style.width = "20%"
        tablesDiv.style.width = "80%"
        tablesDiv.style.marginLeft = "20%"

        tablesDiv.querySelectorAll("*").forEach(element => {
        element.style.width = "68%"

    })

    }
})