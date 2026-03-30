document.addEventListener('DOMContentLoaded', function() {
    var coll = document.getElementsByClassName("collapsible");
    var i;
    console.log("Hello World");
    console.log(coll.length);
    for (i = 0; i < coll.length; i++) {
        console.log(coll[i]);
        coll[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.display === "block") {
            content.style.display = "none";
            } else {
            content.style.display = "block";
            }
        });
    }
    console.log("Filters_Test")
    get_filters_connection()
    var tag_list_master = [];

    function create_all_tags(tag_list){
        // ADDING ALL TAGS - Proof of Concept. Make into function, call for both include and exclude OR copy each entry and apply to both in one??
        // var testing_list = ["obtuse","rubber goose","footloose","I don't know","the rest"]
        const inc_place = document.getElementById('include_div');
        const exc_place = document.getElementById('exclude_div');
        const br = document.createElement('br');
        const iTL_init = document.getElementById('includeTagsList');
        const eTL_init = document.getElementById('excludeTagsList');
        const li_elem = document.createElement("li");
        for (var x = 0; x < tag_list.length; x++) {
            if (x<5) {
                var new_check = document.createElement('input');
                new_check.setAttribute("type","checkbox");
                new_check.setAttribute("name","include_tag");
                new_check.setAttribute("id","include_tag_"+tag_list[x].toLowerCase());
                var new_label = document.createElement('label');
                new_label.setAttribute("for","include_tag_"+tag_list[x].toLowerCase());
                new_label.classList.add("respect_breaks")
                new_label.textContent = tag_list[x]+'\n';
                new_check_clone = new_check.cloneNode(true);
                new_label_clone = new_label.cloneNode(true);
                inc_place.append(new_check);
                inc_place.append(new_label);
                exc_place.append(new_check_clone);
                exc_place.append(new_label_clone);
            }
            // override ul
            var new_li_elem = li_elem.cloneNode(true)
            new_li_elem.textContent = tag_list[x]
            new_li_elem.classList.add('hidden');
            iTL_init.appendChild(new_li_elem)
            var new_li_elem_copy = new_li_elem.cloneNode(true)
            new_li_elem_copy.classList.add('hidden');
            eTL_init.appendChild(new_li_elem_copy)
            tag_list_master.push(tag_list[x])
        }
    }

    var iTL = document.getElementById('includeTagsList');
    var eTL = document.getElementById('excludeTagsList');

    var includeTags = iTL.getElementsByTagName('li');
    var excludeTags = eTL.getElementsByTagName('li');

    // Included Tags Search
    var include_input = document.getElementById("search_include");
    include_input.addEventListener("input", function(){
        // console.log(include_input);
        var to_be_searched = include_input.value.toLowerCase();

        for (var i = 0; i < includeTags.length; i++) {
            var item = includeTags[i];
            var textValue = item.textContent || item.innerText;
            
            if (textValue.toLowerCase().indexOf(to_be_searched) > -1 && to_be_searched!="") {
                item.classList.remove('hidden');
            } else {
                item.classList.add('hidden');
            }
        }
    })
    // Excluded Tags Search
    var exclude_input = document.getElementById("search_exclude");
    exclude_input.addEventListener("input", function(){
        var to_be_searched = exclude_input.value.toLowerCase();

        for (var i = 0; i < excludeTags.length; i++) {
            var item = excludeTags[i];
            var textValue = item.textContent || item.innerText;
            
            if (textValue.toLowerCase().indexOf(to_be_searched) > -1) {
                item.classList.remove('hidden');
            } else {
                item.classList.add('hidden');
            }
        }
    })
    
    // Search
    function set_up_results(results_found) {
        var res_container = document.getElementById("results_container");
        res_container.replaceChildren();
        var new_result_block = document.createElement('div');
        var new_link = document.createElement('a');
        var new_desc = document.createElement('p');

        for (var res_counter = 0; res_counter < results_found.length; res_counter++){
            var clone_result_block = new_result_block.cloneNode(true);
            var clone_link = new_link.cloneNode(true);
            var clone_desc = new_desc.cloneNode(true);
            clone_result_block.classList.add("result_block_long");
            clone_link.setAttribute("href",results_found[res_counter][0]);
            clone_link.textContent = "Title: "+results_found[res_counter][0];
            clone_desc.textContent = "Page(s): "+results_found[res_counter][1]+" - "+results_found[res_counter][2];
            res_container.append(clone_result_block);
            clone_result_block.append(clone_link);
            clone_result_block.append(clone_desc);
        }
    }

    function get_active_filters() {
        var inc_list = [];
        var exc_list = [];
        console.log("tag_list_master length: " + tag_list_master.length)
        for (var check_count = 0; check_count < tag_list_master.length; check_count++) {
            console.log(tag_list_master[check_count])
            var curr_checkbox_inc = document.getElementById("include_tag_"+tag_list_master[check_count].toLowerCase());
            var curr_checkbox_exc = document.getElementById("exclude_tag_"+tag_list_master[check_count].toLowerCase());
            if (curr_checkbox_inc && curr_checkbox_inc.checked) {
                inc_list.push(tag_list_master[check_count]);
                console.log(tag_list_master[check_count])
            }
            if (curr_checkbox_exc && curr_checkbox_exc.checked) {
                exc_list.push(tag_list_master[check_count]);
                console.log(tag_list_master[check_count])
            }
        }
        return inc_list, exc_list;
    }

    function search_archive() {
        console.log("Clicked");
        var query = document.getElementById("searchBar").value;
        var inc_list;
        var exc_list;
        inc_list, exc_list = get_active_filters();
        console.log(query);
        if (inc_list){
            for (var x = 0; x < inc_list.length; x++){
                console.log(inc_list[x]);
            }
        }
        if (exc_list) {
            for (var x = 0; x < exc_list.length; x++){
                console.log(exc_list[x]);
            }
        }
        console.log("About to connect...")
        make_database_connection(query)
    }

    var all_search_buttons = document.getElementsByClassName("search_go");
    for (var search_button_enum = 0; search_button_enum < all_search_buttons.length; search_button_enum++) {
        all_search_buttons[search_button_enum].addEventListener("click", search_archive);
    }

    function make_database_connection(query){
        console.log("using run_search_funct")
        fetch("http://127.0.0.1:5000/run_search_funct", {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            body: JSON.stringify({ message: query })
        })
        .then(response => response.json())
        .then(string => {

            // Printing our response 
            console.log(string);
            console.log(string.answer);
            console.log(string.answer[0]);
            // Printing our field of our response
            console.log(`Title of our response :  ${string.title}`);
            set_up_results(string.answer);
        })
        .catch(errorMsg => { console.log(errorMsg); });
    }

    function get_filters_connection(){
        console.log("using run_filters_funct")
        fetch("http://127.0.0.1:5000/run_filters_funct", {
            method: 'GET',
            headers: {
                "Content-Type": "application/json",
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        })
        .then(response => response.json())
        .then(string => {

            // Printing our response 
            console.log(string);
            console.log(string.answer);
            console.log(string.answer[0]);
            create_all_tags(string.answer)
        })
        .catch(errorMsg => { console.log(errorMsg); });
    }
});