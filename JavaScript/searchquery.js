// To get the query from the textbox and then send it to the Python script
const button = document.getElementById("searchButton");
var query = ""

button.addEventListener("click", function() {
    query = document.getElementById("searchQuery").value;
    // CITE: https://stackoverflow.com/questions/34156282/how-do-i-save-json-to-local-text-file
    var data = {
        searchQuery: query,
        filter: ""
    }
    var jsonData = JSON.stringify(data)

    var fs = require('fs');
    fs.writeFile("test.txt", jsonData, function(err) {
        if (err) {
            console.log(err);
        }
    });
});