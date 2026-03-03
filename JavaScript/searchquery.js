// To get the query from the textbox and then send it to the Python script
const button = document.getElementById("searchButton");
var query = ""

button.addEventListener("click", function() {
    query = document.getElementById("searchQuery").value;
});