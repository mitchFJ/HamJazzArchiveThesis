document.addEventListener('DOMContentLoaded', function() {
    var coll = document.getElementsByClassName("collapsible");
    var collapsi;
    var displayed_tags_inc = 0;
    var displayed_tags_exc = 0;
    var max_displayed_tags = 10;
    console.log("Hello World");
    console.log(coll.length);
    for (collapsi = 0; collapsi < coll.length; collapsi++) {
        console.log(coll[collapsi]);
        coll[collapsi].addEventListener("click", function() {
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
    const inc_place = document.getElementById('include_div');
    const exc_place = document.getElementById('exclude_div');

    function create_all_tags(tag_list){
        // ADDING ALL TAGS
        const br = document.createElement('br');
        const iTL_init = document.getElementById('includeTagsList');
        const eTL_init = document.getElementById('excludeTagsList');
        const li_elem = document.createElement("li");
        for (var x = 0; x < tag_list.length; x++) {
            var new_check = document.createElement('input');
            new_check.setAttribute("type","checkbox");
            new_check.setAttribute("name","include_tag");
            new_check.setAttribute("id","include_tag_"+tag_list[x].toLowerCase());
            var new_label = document.createElement('label');
            new_label.setAttribute("id","include_label_"+tag_list[x].toLowerCase());
            new_label.setAttribute("for","include_tag_"+tag_list[x].toLowerCase());
            new_label.classList.add("respect_breaks")
            new_label.textContent = tag_list[x]+'\n';
            if (x>4){
                new_check.classList.add("hidden")
                new_label.classList.add("hidden")
            }
            else{
                displayed_tags_inc+=1;
                console.log("Disp_tags_inc"+displayed_tags_inc)
                displayed_tags_exc+=1;
            }
            new_check_clone = new_check.cloneNode(true);
            new_label_clone = new_label.cloneNode(true);
            // Make sure to update names and ids for exclude
            // lol forgot to do this before testing no wonder
            new_check_clone.setAttribute("name","exclude_tag");
            new_check_clone.setAttribute("id","exclude_tag_"+tag_list[x].toLowerCase());
            new_label_clone.setAttribute("id","exclude_label_"+tag_list[x].toLowerCase());
            new_label_clone.setAttribute("for","exclude_tag_"+tag_list[x].toLowerCase());
            // And append, having updated for exclude
            inc_place.append(new_check);
            inc_place.append(new_label);
            exc_place.append(new_check_clone);
            exc_place.append(new_label_clone);
            
            // override ul
            var new_li_elem = li_elem.cloneNode(true);
            new_li_elem.textContent = tag_list[x];
            new_li_elem.classList.add('hidden');
            new_li_elem.classList.add('searchedTagItem');
            iTL_init.appendChild(new_li_elem);
            var new_li_elem_copy = new_li_elem.cloneNode(true);
            //new_li_elem_copy.classList.add('hidden');
            eTL_init.appendChild(new_li_elem_copy);
            tag_list_master.push(tag_list[x]);
        }
    }

    var iTL = document.getElementById('includeTagsList');
    var eTL = document.getElementById('excludeTagsList');

    // Detect new tag selection from tag search
    iTL.addEventListener('click', function(event){
        const searched_li_elem = event.target;
        const searched_text_cont = searched_li_elem.textContent;
        // prepending and appending removes from cuur loc in elem
        var clicked_tag_to_be_shown = document.getElementById("include_tag_"+searched_text_cont.toLowerCase());
        var clicked_label_to_be_shown = document.getElementById("include_label_"+searched_text_cont.toLowerCase());
        clicked_tag_to_be_shown.classList.remove('hidden');
        clicked_label_to_be_shown.classList.remove('hidden');
        displayed_tags_inc+=1;
        // console.log("Disp_tags_inc"+displayed_tags_inc)
        clicked_tag_to_be_shown.checked = !clicked_tag_to_be_shown.checked;
        // Puts it at top if newly checked
        if (clicked_tag_to_be_shown.checked){
            inc_place.insertBefore(clicked_label_to_be_shown,inc_place.children[2])
            inc_place.insertBefore(clicked_tag_to_be_shown,inc_place.children[2])
        }
        include_input.value="";
        inc_disp_tags();
        if (displayed_tags_inc>=max_displayed_tags && !inc_place.children[displayed_tags_inc*2].checked){
            console.log("Removing tag from visible: " + inc_place.children[displayed_tags_inc*2].id);
            console.log("Removing corresponding label: " + inc_place.children[displayed_tags_inc*2+1].id);
            inc_place.children[displayed_tags_inc*2].classList.add("hidden");
            inc_place.children[displayed_tags_inc*2+1].classList.add("hidden");
            displayed_tags_inc-=1;
        }
    });
    // Exclude ver
    eTL.addEventListener('click', function(event){
        const searched_li_elem = event.target;
        const searched_text_cont = searched_li_elem.textContent;
        // prepending and appending removes from cuur loc in elem
        var clicked_tag_to_be_shown = document.getElementById("exclude_tag_"+searched_text_cont.toLowerCase());
        var clicked_label_to_be_shown = document.getElementById("exclude_label_"+searched_text_cont.toLowerCase());
        clicked_tag_to_be_shown.classList.remove('hidden');
        clicked_label_to_be_shown.classList.remove('hidden');
        displayed_tags_exc+=1;
        console.log("Disp_tags_exc"+displayed_tags_exc)
        clicked_tag_to_be_shown.checked = !clicked_tag_to_be_shown.checked;
        // Puts it at top if newly checked
        if (clicked_tag_to_be_shown.checked){
            exc_place.insertBefore(clicked_label_to_be_shown,exc_place.children[2])
            exc_place.insertBefore(clicked_tag_to_be_shown,exc_place.children[2])
        }
        exclude_input.value="";
        exc_disp_tags();
        if (displayed_tags_exc>=max_displayed_tags && !exc_place.children[displayed_tags_exc*2].checked){
            console.log("Removing tag from visible: " + exc_place.children[displayed_tags_exc*2].id);
            console.log("Removing corresponding label: " + exc_place.children[displayed_tags_exc*2+1].id);
            exc_place.children[displayed_tags_exc*2].classList.add("hidden");
            exc_place.children[displayed_tags_exc*2+1].classList.add("hidden");
            displayed_tags_exc-=1;
        }
    });
    // balance
    inc_place.addEventListener('click', function(event){
        const clicked_inc_elem = event.target;
        const id_pref = clicked_inc_elem.id.substring(0,12);
        const id_spef = clicked_inc_elem.id.substring(12)
        // console.log("Id: "+clicked_inc_elem.id)
        // console.log("Id: "+clicked_inc_elem.id.substring(0,12))
        // console.log("Id: "+clicked_inc_elem.id.substring(12))
        // console.log("Disp_tags_inc"+displayed_tags_inc)
        if (id_pref == "include_tag_"){
            incl_tag_focused = clicked_inc_elem
            incl_label_focused = document.getElementById("include_label_"+id_spef)
            if (clicked_inc_elem.checked){
                inc_place.insertBefore(incl_label_focused,inc_place.children[2]);
                inc_place.insertBefore(incl_tag_focused,inc_place.children[2]);
            }
            else{
                if (displayed_tags_inc<max_displayed_tags){

                    var index_of_tag_focused = Array.prototype.indexOf.call(inc_place.children, incl_tag_focused);
                    var index_of_label_focused = index_of_tag_focused+1;
                    var target_of_tag_focused = max_displayed_tags*2;
                    var target_of_label_focused = max_displayed_tags*2+1;
                    var found_space = false;
                    var iterable_unfocused = index_of_tag_focused + 2;

                    console.log(index_of_tag_focused)
                    while (!found_space && iterable_unfocused<displayed_tags_inc*2+2) {
                        // console.log("Curr Box: " + inc_place.children[iterable_unfocused].id + ", " + iterable_unfocused);
                        if (!inc_place.children[iterable_unfocused].checked){
                            found_space = true;
                            target_of_tag_focused = iterable_unfocused;
                            target_of_label_focused = iterable_unfocused+1;
                            // console.log("New: "+target_of_tag_focused+", "+target_of_label_focused)
                        }
                        iterable_unfocused+=2;
                    }
                    // console.log("Inserting before " + incl_label_focused,inc_place.children[target_of_tag_focused].id)
                    inc_place.insertBefore(incl_tag_focused,inc_place.children[target_of_tag_focused]);
                    // console.log("Inserting before " + incl_label_focused,inc_place.children[target_of_tag_focused].id)
                    inc_place.insertBefore(incl_label_focused,inc_place.children[target_of_tag_focused]);
                    // console.log("Ending Box: " + inc_place.children[target_of_tag_focused].id);
                    // console.log("Ending Label: " + inc_place.children[target_of_label_focused].id);

                }
                else{
                    var index_of_tag_focused = Array.prototype.indexOf.call(inc_place.children, incl_tag_focused);
                    var index_of_label_focused = index_of_tag_focused+1;
                    var target_of_tag_focused = displayed_tags_inc*2+2;
                    var target_of_label_focused = displayed_tags_inc*2+3;

                    inc_place.insertBefore(incl_label_focused,inc_place.children[target_of_label_focused]);
                    inc_place.insertBefore(incl_tag_focused,inc_place.children[target_of_tag_focused]);
                    // console.log("Ending Box: " + inc_place.children[displayed_tags_inc*2+1].id);
                    // console.log("Ending Label: " + inc_place.children[displayed_tags_inc*2+2].id);
                    inc_place.children[displayed_tags_inc*2+1].classList.add("hidden")
                    inc_place.children[displayed_tags_inc*2+2].classList.add("hidden")
                    displayed_tags_inc-=1;
                    // console.log("Displayed Tags Inc: "+displayed_tags_inc);
                }
            }
        }
    });
    // ... and the exclude version:
    exc_place.addEventListener('click', function(event){
        const clicked_exc_elem = event.target;
        const id_pref = clicked_exc_elem.id.substring(0,12);
        const id_spef = clicked_exc_elem.id.substring(12)
        console.log("Here where I want to be, "+ id_pref)
        console.log("Id: "+clicked_exc_elem.id)
        console.log("Id: "+clicked_exc_elem.id.substring(0,12))
        console.log("Id: "+clicked_exc_elem.id.substring(12))
        console.log("Disp_tags_exc"+displayed_tags_exc)
        if (id_pref == "exclude_tag_"){
            excl_tag_focused = clicked_exc_elem
            excl_label_focused = document.getElementById("exclude_label_"+id_spef)
            if (clicked_exc_elem.checked){
                exc_place.insertBefore(excl_label_focused,exc_place.children[2]);
                exc_place.insertBefore(excl_tag_focused,exc_place.children[2]);
            }
            else{
                if (displayed_tags_exc<max_displayed_tags){

                    var index_of_tag_focused = Array.prototype.indexOf.call(exc_place.children, excl_tag_focused);
                    var index_of_label_focused = index_of_tag_focused+1;
                    var target_of_tag_focused = max_displayed_tags*2;
                    var target_of_label_focused = max_displayed_tags*2+1;
                    var found_space = false;
                    var iterable_unfocused = index_of_tag_focused + 2;

                    console.log(index_of_tag_focused)
                    while (!found_space && iterable_unfocused<displayed_tags_exc*2+2) {
                        console.log("Curr Box: " + exc_place.children[iterable_unfocused].id + ", " + iterable_unfocused);
                        if (!exc_place.children[iterable_unfocused].checked){
                            found_space = true;
                            target_of_tag_focused = iterable_unfocused;
                            target_of_label_focused = iterable_unfocused+1;
                            console.log("New: "+target_of_tag_focused+", "+target_of_label_focused)
                        }
                        iterable_unfocused+=2;
                    }
                    console.log("Inserting before " + excl_label_focused,exc_place.children[target_of_tag_focused].id)

                    exc_place.insertBefore(excl_tag_focused,exc_place.children[target_of_tag_focused]);
                    console.log("Inserting before " + excl_label_focused,exc_place.children[target_of_tag_focused].id)
                    exc_place.insertBefore(excl_label_focused,exc_place.children[target_of_tag_focused]);
                    console.log("Ending Box: " + exc_place.children[target_of_tag_focused].id);
                    console.log("Ending Label: " + exc_place.children[target_of_label_focused].id);

                }
                else{
                    var index_of_tag_focused = Array.prototype.indexOf.call(exc_place.children, excl_tag_focused);
                    var index_of_label_focused = index_of_tag_focused+1;
                    var target_of_tag_focused = displayed_tags_exc*2+2;
                    var target_of_label_focused = displayed_tags_exc*2+3;

                    exc_place.insertBefore(excl_label_focused,exc_place.children[target_of_label_focused]);
                    exc_place.insertBefore(excl_tag_focused,exc_place.children[target_of_tag_focused]);
                    console.log("Ending Box: " + exc_place.children[displayed_tags_exc*2+1].id);
                    console.log("Ending Label: " + exc_place.children[displayed_tags_exc*2+2].id);
                    exc_place.children[displayed_tags_exc*2+1].classList.add("hidden")
                    exc_place.children[displayed_tags_exc*2+2].classList.add("hidden")
                    displayed_tags_exc-=1
                    console.log("Displayed Tags Exc: "+displayed_tags_exc);
                }
            }
        }
    });

    var includeTags = iTL.getElementsByTagName('li');
    var excludeTags = eTL.getElementsByTagName('li');

    // Included Tags Search
    var include_input = document.getElementById("search_include");
    include_input.addEventListener("input",inc_disp_tags);
    function inc_disp_tags(){
        var to_be_searched = include_input.value.toLowerCase();
        console.log(to_be_searched);

        for (var i = 0; i < includeTags.length; i++) {
            var item = includeTags[i];
            var textValue = item.textContent || item.innerText;
            
            if (textValue.toLowerCase().indexOf(to_be_searched) > -1 && to_be_searched!="") {
                item.classList.remove('hidden');
            } else {
                item.classList.add('hidden');
            }
        }
    }
    // Excluded Tags Search
    var exclude_input = document.getElementById("search_exclude");
    exclude_input.addEventListener("input", exc_disp_tags);
    function exc_disp_tags(){
        var to_be_searched = exclude_input.value.toLowerCase();
        console.log(to_be_searched);

        for (var i = 0; i < excludeTags.length; i++) {
            var item = excludeTags[i];
            var textValue = item.textContent || item.innerText;
            
            if (textValue.toLowerCase().indexOf(to_be_searched) > -1 && to_be_searched!="") {
                item.classList.remove('hidden');
            } else {
                item.classList.add('hidden');
            }
        }
    }

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
            //console.log(tag_list_master[check_count])
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
        console.log("inc_list len"+inc_list.length)
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