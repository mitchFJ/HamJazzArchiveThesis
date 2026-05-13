document.addEventListener('DOMContentLoaded', function() {
    var coll = document.getElementsByClassName("collapsible");
    var collapsi;
    var max_init_display = 5;
    var displayed_tags_inc = 0;
    var inc_checked_counter = 0;
    var inc_showing_more = false;
    var displayed_tags_exc = 0;
    var exc_checked_counter = 0;
    var exc_showing_more = false;

    var max_displayed_tags = 5;

    var FULL_RESULTS = []
    var max_results_displayed = 10;
    var curr_first_result = 0;
    var page_buttons_loaded = false;
    var MAX_RESULTS = 99;

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

    // Disables 'Exclude' tag filter
    // coll[1].classList.add("hidden");

    var isTabbing = false;
    window.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            isTabbing = true;
        }
    });
    window.addEventListener('mousedown', () => {
        isTabbing = false;
    });
    window.addEventListener('focusin', () => {
        if (isTabbing) {
            console.log('Focused by Tab:', document.activeElement);
        }
    });


    document.addEventListener("keydown", function(e) {
        if (isTabbing && e.key === "Enter" && !document.activeElement.classList.contains("collapsible")) {
            e.preventDefault();
            document.activeElement.click();
        }
    });


    function create_all_tags(tag_list){
        // ADDING ALL TAGS
        tag_list.sort();
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
            if (x>=max_init_display){
                new_check.classList.add("hidden");
                new_label.classList.add("hidden");
            }
            else{
                displayed_tags_inc+=1;
                console.log("Disp_tags_inc"+displayed_tags_inc)
                displayed_tags_exc+=1;
            }
            new_check_clone = new_check.cloneNode(true);
            new_label_clone = new_label.cloneNode(true);
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
            new_li_elem.setAttribute("tabindex","0")
            iTL_init.appendChild(new_li_elem);
            var new_li_elem_copy = new_li_elem.cloneNode(true);
            eTL_init.appendChild(new_li_elem_copy);
            tag_list_master.push(tag_list[x]);
        }
        var show_inc_button = document.createElement("button");
        show_inc_button.classList.add("show_more_button");
        show_inc_button.textContent = "Show More ("+(tag_list.length-max_init_display)+")";
        var show_exc_button = show_inc_button.cloneNode(true);
        inc_place.appendChild(show_inc_button);
        exc_place.appendChild(show_exc_button);
        show_inc_button.addEventListener('click', function(){
            var place_children = Array.from(inc_place.children).slice(2,inc_place.children.length-1);
            for (var index = 0; index < place_children.length; index++){
                if (place_children[index].classList.contains("hidden") && !inc_showing_more){
                    place_children[index].classList.remove("hidden");
                    show_inc_button.textContent = "Show Less";
                }
                else if(index>displayed_tags_inc*2-1 && inc_showing_more) {
                    place_children[index].classList.add("hidden");
                    show_inc_button.textContent = "Show More ("+(tag_list.length-max_init_display)+")";
                }
            }
            inc_showing_more = !inc_showing_more;
        })
        show_exc_button.addEventListener('click', function(){
            var place_children = Array.from(exc_place.children).slice(2,exc_place.children.length-1);
            for (var index = 0; index < place_children.length; index++){
                if (place_children[index].classList.contains("hidden") && !exc_showing_more){
                    place_children[index].classList.remove("hidden");
                    show_exc_button.textContent = "Show Less";
                }
                else if(index>displayed_tags_exc*2-1 && exc_showing_more) {
                    place_children[index].classList.add("hidden");
                    show_exc_button.textContent = "Show More ("+(tag_list.length-max_init_display)+")";
                }
            }
            exc_showing_more = !exc_showing_more;
        })
    }

    var iTL = document.getElementById('includeTagsList');
    var eTL = document.getElementById('excludeTagsList');

    // Detect new tag selection from tag search
    iTL.addEventListener('click', function(event){
        const searched_li_elem = event.target;
        const searched_text_cont = searched_li_elem.textContent;
        // prepending and appending removes from curr loc in elem
        var clicked_tag_to_be_shown = document.getElementById("include_tag_"+searched_text_cont.toLowerCase());
        var clicked_label_to_be_shown = document.getElementById("include_label_"+searched_text_cont.toLowerCase());
        clicked_tag_to_be_shown.classList.remove('hidden');
        clicked_label_to_be_shown.classList.remove('hidden');
        clicked_tag_to_be_shown.click();
        if (clicked_tag_to_be_shown.checked){
            displayed_tags_inc+=1;
        }
        include_input.value="";
        inc_disp_tags();
    });
    // Exclude ver
    eTL.addEventListener('click', function(event){
        const searched_li_elem = event.target;
        const searched_text_cont = searched_li_elem.textContent;
        var clicked_tag_to_be_shown = document.getElementById("exclude_tag_"+searched_text_cont.toLowerCase());
        var clicked_label_to_be_shown = document.getElementById("exclude_label_"+searched_text_cont.toLowerCase());
        clicked_tag_to_be_shown.classList.remove('hidden');
        clicked_label_to_be_shown.classList.remove('hidden');
        clicked_tag_to_be_shown.click();
        if (clicked_tag_to_be_shown.checked){
            displayed_tags_exc+=1;
        }
        exclude_input.value="";
        exc_disp_tags();
    });

    // balance
    inc_place.addEventListener('click', function(event){
        const clicked_inc_elem = event.target;
        const id_pref = clicked_inc_elem.id.substring(0,12);
        const id_spef = clicked_inc_elem.id.substring(12)
        if (id_pref == "include_tag_"){
            incl_tag_focused = clicked_inc_elem;
            incl_label_focused = document.getElementById("include_label_"+id_spef);
            if (clicked_inc_elem.checked){
                if (inc_showing_more){
                    displayed_tags_inc+=1;
                }
                inc_checked_counter+=1;
                document.startViewTransition(() => {
                    inc_place.insertBefore(incl_label_focused,inc_place.children[2]);
                    inc_place.insertBefore(incl_tag_focused,inc_place.children[2]);
                });
            }
            else{
                incl_tag_focused = clicked_inc_elem;
                incl_label_focused = document.getElementById("include_label_"+id_spef);
                var temp_inc_plac_chil = Array.from(inc_place.children).slice(2+(inc_checked_counter*2),inc_place.children.length-1);
                for (var inc_lab_ind = 0; inc_lab_ind < temp_inc_plac_chil.length; inc_lab_ind++){
                    if (inc_lab_ind%2!=0){
                        if (temp_inc_plac_chil[inc_lab_ind].id>incl_label_focused.id){
                            inc_place.insertBefore(incl_label_focused,inc_place.children[inc_lab_ind+1+inc_checked_counter*2]);
                            inc_place.insertBefore(incl_tag_focused,inc_place.children[inc_lab_ind+inc_checked_counter*2]);
                            if (displayed_tags_inc*2>max_displayed_tags*2 && !inc_showing_more){
                                incl_tag_focused.classList.add("hidden");
                                incl_label_focused.classList.add("hidden");
                                displayed_tags_inc-=1;
                            }
                            break;
                        }
                    }
                }
                inc_checked_counter-=1;
            }
        }
    });
    // ... and the exclude version:
    exc_place.addEventListener('click', function(event){
        const clicked_exc_elem = event.target;
        const id_pref = clicked_exc_elem.id.substring(0,12);
        const id_spef = clicked_exc_elem.id.substring(12)
        if (id_pref == "exclude_tag_"){
            excl_tag_focused = clicked_exc_elem;
            excl_label_focused = document.getElementById("exclude_label_"+id_spef);
            if (clicked_exc_elem.checked){
                if (exc_showing_more){
                    displayed_tags_exc+=1;
                }
                exc_checked_counter+=1;
                document.startViewTransition(() => {
                    exc_place.insertBefore(excl_label_focused,exc_place.children[2]);
                    exc_place.insertBefore(excl_tag_focused,exc_place.children[2]);
                });
            }
            else{
                excl_tag_focused = clicked_exc_elem;
                excl_label_focused = document.getElementById("exclude_label_"+id_spef);
                var temp_exc_plac_chil = Array.from(exc_place.children).slice(2+(exc_checked_counter*2),exc_place.children.length-1);
                for (var exc_lab_ind = 0; exc_lab_ind < temp_exc_plac_chil.length; exc_lab_ind++){
                    if (exc_lab_ind%2!=0){
                        if (temp_exc_plac_chil[exc_lab_ind].id>excl_label_focused.id){
                            exc_place.insertBefore(excl_label_focused,exc_place.children[exc_lab_ind+1+exc_checked_counter*2]);
                            exc_place.insertBefore(excl_tag_focused,exc_place.children[exc_lab_ind+exc_checked_counter*2]);
                            if (displayed_tags_exc*2>max_displayed_tags*2 && !exc_showing_more){
                                excl_tag_focused.classList.add("hidden");
                                excl_label_focused.classList.add("hidden");
                                displayed_tags_exc-=1;
                            }
                            break;
                        }
                    }
                }
                exc_checked_counter-=1;
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
        var is_even = false;

        var curr_last_result = (curr_first_result+max_results_displayed)
        if (curr_last_result > results_found.length){
            curr_last_result = results_found.length;
        }

        var show_res_num = document.createElement('p');
        show_res_num.setAttribute("id","show_res_num");
        show_res_num.textContent = results_found.length + " results found. Displaying page "+((curr_first_result/max_results_displayed)+1)+" of "+Math.ceil(FULL_RESULTS.length/max_results_displayed)+"; Results "+(curr_first_result+1)+" - " + (curr_last_result) + ".";
        res_container.append(show_res_num)

        for (var res_counter = 0; res_counter < max_results_displayed && res_counter+curr_first_result<curr_last_result; res_counter++){
            var clone_result_block = new_result_block.cloneNode(true);
            var clone_link = new_link.cloneNode(true);
            var clone_desc = new_desc.cloneNode(true);
            if (is_even){
                clone_result_block.classList.add("result_block_long_alt");
            }
            else {
                clone_result_block.classList.add("result_block_long");
            }
            is_even = !is_even;
            clone_link.setAttribute("href",results_found[res_counter + curr_first_result][1]);
            clone_link.setAttribute("target","_blank");
            clone_link.setAttribute("rel","noopener noreferrer");
            clone_link.textContent = results_found[res_counter + curr_first_result][0];
            clone_desc.textContent = "Page(s): "+results_found[res_counter + curr_first_result][2]+" - "+results_found[res_counter + curr_first_result][3];
            clone_desc.innerHTML = clone_desc.innerHTML.replace(
                results_found[res_counter + curr_first_result][4], 
                `<mark>${results_found[res_counter + curr_first_result][4]}</mark>`
            );

            res_container.append(clone_result_block);
            clone_result_block.append(clone_link);
            clone_result_block.append(clone_desc);
        }
        console.log("---------------------")
        console.log(FULL_RESULTS[0][0])
        console.log(FULL_RESULTS[0][1])
        console.log(FULL_RESULTS[0][2])
        console.log(FULL_RESULTS[0][3])
        console.log(FULL_RESULTS[0][4])
        console.log(FULL_RESULTS[0][5])
        console.log("---------------------")

        if (!page_buttons_loaded && results_found.length>max_results_displayed){
            const pb_div = document.createElement('div')
            pb_div.classList.add("page_butt_holder")
            document.body.insertBefore(pb_div, document.body.children[document.body.children.length-1])

            var base_page_butt = document.createElement("button");
            base_page_butt.classList.add("page_button");
            var base_page_butt_plac = document.createElement("p");
            base_page_butt_plac.classList.add("page_butt_plac");
            base_page_butt_plac.classList.add("hidden");

            var clone_prev_butt = base_page_butt.cloneNode(true);
            clone_prev_butt.textContent = "<- Prev"
            var clone_prev_plac = base_page_butt_plac.cloneNode(true);
            clone_prev_plac.textContent = "<- Prev"

            clone_prev_butt.addEventListener("click", function(event){
                if (((curr_first_result/max_results_displayed)-1)*max_results_displayed >= 0)
                    curr_first_result = ((curr_first_result/max_results_displayed)-1)*max_results_displayed;

                    var ind_of_page = (curr_first_result/max_results_displayed)+1;
                    // displays newly selected page's text equiv and hides others.
                    var only_placs = document.getElementsByClassName("page_butt_plac");
                    only_placs = Array.from(only_placs)
                    for (var pag_but_ind in only_placs) {
                        var pag_but_plac = only_placs[pag_but_ind]
                        if (pag_but_plac.textContent == ind_of_page || (ind_of_page == 1 && pag_but_plac.textContent == "<- Prev") || (ind_of_page == Math.ceil(FULL_RESULTS.length/max_results_displayed) && pag_but_plac.textContent == "Next ->")){
                            pag_but_plac.classList.remove("hidden")
                        }
                        else if (!pag_but_plac.classList.contains("hidden")){
                            pag_but_plac.classList.add("hidden");
                        }
                    }
                    
                    // swaps selected page button for previously selected page button
                    var only_buttons = document.getElementsByClassName("page_button");
                    only_buttons = Array.from(only_buttons)
                    
                    for (var pag_but_ind in only_buttons) {
                        var pag_but = only_buttons[pag_but_ind]
                        if (pag_but.textContent == ind_of_page || (ind_of_page == 1 && pag_but.textContent == "<- Prev") || (ind_of_page == Math.ceil(FULL_RESULTS.length/max_results_displayed) && pag_but.textContent == "Next ->")){
                            pag_but.classList.add("hidden")
                        }
                        else if (pag_but.classList.contains("hidden")){
                            pag_but.classList.remove("hidden");
                        }
                    }
                set_up_results(FULL_RESULTS);
            });

            // Because we always start on page 1:
            clone_prev_butt.classList.add("hidden");
            clone_prev_plac.classList.remove("hidden");
            // Add to document
            pb_div.appendChild(clone_prev_butt);
            pb_div.appendChild(clone_prev_plac);

            for (var page_num = 1; page_num <= Math.ceil(results_found.length/max_results_displayed); page_num++){
                var clone_page_butt = base_page_butt.cloneNode(true);
                clone_page_butt.textContent = page_num;
                var clone_page_plac = base_page_butt_plac.cloneNode(true);
                clone_page_plac.textContent = page_num;

                clone_page_butt.addEventListener("click", function(event){
                    var clicked_button = event.target;
                    curr_first_result = (event.target.textContent-1)*max_results_displayed;
                    // displays newly selected page's text equiv and hides others.
                    var only_placs = document.getElementsByClassName("page_butt_plac");
                    only_placs = Array.from(only_placs)
                    for (var pag_but_ind in only_placs) {
                        var pag_but_plac = only_placs[pag_but_ind]
                        if (pag_but_plac.textContent == clicked_button.textContent || (clicked_button.textContent == 1 && pag_but_plac.textContent == "<- Prev") || (clicked_button.textContent == Math.ceil(FULL_RESULTS.length/max_results_displayed) && pag_but_plac.textContent == "Next ->")){
                            pag_but_plac.classList.remove("hidden")
                        }
                        else if (!pag_but_plac.classList.contains("hidden")){
                            pag_but_plac.classList.add("hidden");
                        }
                    }
                    
                    // swaps selected page button for previously selected page button
                    var only_buttons = document.getElementsByClassName("page_button");
                    only_buttons = Array.from(only_buttons)
                    
                    for (var pag_but_ind in only_buttons) {
                        var pag_but = only_buttons[pag_but_ind]
                        if (pag_but.textContent == clicked_button.textContent || (clicked_button.textContent == 1 && pag_but.textContent == "<- Prev") || (clicked_button.textContent == Math.ceil(FULL_RESULTS.length/max_results_displayed) && pag_but.textContent == "Next ->")){
                            pag_but.classList.add("hidden")
                        }
                        else if (pag_but.classList.contains("hidden")){
                            pag_but.classList.remove("hidden");
                        }
                    }
                    set_up_results(FULL_RESULTS);
                });
                // again, because we start on page 1
                if (page_num == 1){
                    clone_page_butt.classList.add("hidden");
                    clone_page_plac.classList.remove("hidden");
                }
                pb_div.appendChild(clone_page_butt);
                pb_div.appendChild(clone_page_plac);
            }

            var clone_next_butt = base_page_butt.cloneNode(true);
            clone_next_butt.textContent = "Next ->"
            var clone_next_plac = base_page_butt_plac.cloneNode(true);
            clone_next_plac.textContent = "Next ->"
            clone_next_butt.addEventListener("click", function(event){
                if (((curr_first_result/max_results_displayed)+1)*max_results_displayed < results_found.length){
                    curr_first_result = ((curr_first_result/max_results_displayed)+1)*max_results_displayed;

                    var ind_of_page = (curr_first_result/max_results_displayed)+1;
                    // displays newly selected page's text equiv and hides others.
                    var only_placs = document.getElementsByClassName("page_butt_plac");
                    only_placs = Array.from(only_placs);
                    console.log(ind_of_page);
                    for (var pag_but_ind in only_placs) {
                        var pag_but_plac = only_placs[pag_but_ind];
                        console.log(pag_but_plac.textContent);
                        if (pag_but_plac.textContent == ind_of_page || (ind_of_page == 1 && pag_but_plac.textContent == "<- Prev") || (ind_of_page == Math.ceil(FULL_RESULTS.length/max_results_displayed) && pag_but_plac.textContent == "Next ->")){
                            console.log("Functional on "+pag_but_plac.textContent+".")
                            pag_but_plac.classList.remove("hidden")
                        }
                        else if (!pag_but_plac.classList.contains("hidden")){
                            pag_but_plac.classList.add("hidden");
                        }
                    }
                    
                    // swaps selected page button for previously selected page button
                    var only_buttons = document.getElementsByClassName("page_button");
                    only_buttons = Array.from(only_buttons)
                    
                    console.log(ind_of_page)
                    for (var pag_but_ind in only_buttons) {
                        var pag_but = only_buttons[pag_but_ind]
                        console.log(pag_but.textContent)
                        console.log(pag_but.textContent == ind_of_page)
                        if (pag_but.textContent == ind_of_page || (ind_of_page == 1 && pag_but.textContent == "<- Prev") || (ind_of_page == Math.ceil(FULL_RESULTS.length/max_results_displayed) && pag_but.textContent == "Next ->")){
                            console.log("Functional on "+pag_but.textContent+".")
                            pag_but.classList.add("hidden")
                        }
                        else if (pag_but.classList.contains("hidden")){
                            pag_but.classList.remove("hidden");
                        }
                    }

                    set_up_results(FULL_RESULTS);
                }
            });
            pb_div.appendChild(clone_next_butt);
            pb_div.appendChild(clone_next_plac);

            page_buttons_loaded = true;
        }
    }

    function get_active_filters() {
        var inc_list = [];
        var exc_list = [];
        console.log("tag_list_master length: " + tag_list_master.length)
        for (var check_count = 0; check_count < tag_list_master.length; check_count++) {
            var curr_checkbox_inc = document.getElementById("include_tag_"+tag_list_master[check_count].toLowerCase());
            var curr_checkbox_exc = document.getElementById("exclude_tag_"+tag_list_master[check_count].toLowerCase());
            if (curr_checkbox_inc && curr_checkbox_inc.checked) {
                inc_list.push(tag_list_master[check_count]);
                console.log(tag_list_master[check_count])
            }
            if (curr_checkbox_exc && curr_checkbox_exc.checked) {
                exc_list.push(tag_list_master[check_count]);
                console.log(tag_list_master[check_count]);
            }
        }
        console.log("inc_list len"+inc_list.length);
        return {inc_list, exc_list};
    }

    function search_archive() {
        console.log("Clicked");
        var res_container = document.getElementById("results_container");
        res_container.replaceChildren();
        
        var loading_results = document.createElement('p');
        loading_results.textContent = "Loading...";
        res_container.append(loading_results)

        if (page_buttons_loaded) {
            var pb_cont = document.getElementsByClassName("page_butt_holder")[0];
            document.body.removeChild(pb_cont);
            page_buttons_loaded = false;
        }

        var query = document.getElementById("searchBar").value;
        var {inc_list: inc_list_master, exc_list: exc_list_master} = get_active_filters();
        console.log(query);
        console.log(inc_list_master)
        if (inc_list_master){
            // console.log("inc_list_master in search_archive()")
            for (var x = 0; x < inc_list_master.length; x++){
                console.log("   "+inc_list_master[x]);
            }
        }
        if (exc_list_master) {
            // console.log("inc_list_master in search_archive()")
            for (var x = 0; x < exc_list_master.length; x++){
                console.log("   "+exc_list_master[x]);
            }
        }
        console.log("About to connect...")
        make_database_connection(query, inc_list_master, exc_list_master)
    }

    var all_search_buttons = document.getElementsByClassName("search_go");
    for (var search_button_enum = 0; search_button_enum < all_search_buttons.length; search_button_enum++) {
        all_search_buttons[search_button_enum].addEventListener("click", search_archive);
    }
    document.getElementById("searchBar").addEventListener('keydown', function(event){
        if (event.key == 'Enter'){
            this.blur();
            search_archive();
        }
    })

    function make_database_connection(query, inc_list, exc_list){
        console.log("using run_search_funct")
        fetch("http://127.0.0.1:5000/run_search_funct", {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            body: JSON.stringify({ message: query, inc_list_json_ver: inc_list, exc_list_json_ver: exc_list, glob_num_ret: MAX_RESULTS})
        })
        .then(response => response.json())
        .then(string => {

            // Printing our response 
            console.log(string);
            console.log(string.answer);
            console.log(string.answer[0]);
            // Printing our field of our response
            console.log(`Title of our response :  ${string.title}`);
            FULL_RESULTS = string.answer;
            curr_first_result = 0;
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