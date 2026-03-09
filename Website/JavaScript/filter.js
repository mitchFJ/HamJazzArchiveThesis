// To select paramaters, store parameter information, and then send parameter informatin to Python script
// Reagan Example
function get_active_filters() {
    var inc_list = [];
    var exc_list = [];
    for (var check_count = 0; check_count < testing_list.length; check_count++) {
        var curr_checkbox_inc = document.getElementById("include_tag_"+testing_list[check_count].toLowerCase());
        var curr_checkbox_exc = document.getElementById("exclude_tag_"+testing_list[check_count].toLowerCase());
        if (curr_checkbox_inc && curr_checkbox_inc.checked) {
            inc_list.push(testing_list[check_count]);
            console.log(testing_list[check_count])
        }
        if (curr_checkbox_exc && curr_checkbox_exc.checked) {
            exc_list.push(testing_list[check_count]);
            console.log(testing_list[check_count])
        }
    }
    return inc_list, exc_list;
}