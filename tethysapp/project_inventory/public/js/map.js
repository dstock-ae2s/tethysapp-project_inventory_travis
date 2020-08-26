function saveDataToDB () {

    var facility_id = (document.getElementById('modal-facility-id').innerHTML).replace("Facility ID: ","");
    console.log((document.getElementById('modal-facility-id').value));
    var location = document.getElementById('modal-facility-id').value;
    var latitude = location[0];
    var longitude = location[1];

    console.log(facility_id);
    var proj_name_list = [];
    var proj_est_cost_list = [];
    var proj_const_year_list = [];
    var proj_category_list = [];
    var proj_description_list = [];
    var proj_priority_list = [];
    var proj_const_cost_list = [];
    var proj_est_year_list = [];
    var debt_checkbox_list = [];
    var recur_checkbox_list = [];

    var project_names = document.querySelectorAll('.project-name');

    for (var i = 1; i <= project_names.length; i++) {

        project_name = document.getElementById( i+'-project-name').value;
        est_cost = document.getElementById(i+'-project-estcost').value;
        est_cost = currencyToNumber(document.getElementById(i+'-project-estcost').value);


        const_year = document.getElementById(i+'-project-constyear').value;
        category = document.getElementById(i+'-project-category').value;
        description = document.getElementById(i+'-project-description').value;
        priority = document.getElementById(i+'-project-priority').value;
        const_cost = document.getElementById(i+'-project-constcost').value;
        const_cost = currencyToNumber(document.getElementById(i+'-project-constcost').value);

        est_year = document.getElementById(i+'-project-estyear').value;
        debt_is_checkbox = document.getElementById(i+'-debt-checkbox');
        recur_is_checkbox = document.getElementById(i+'-recur-checkbox');

        if (debt_is_checkbox.checked==true){
            debt_is_checkbox=true;
        } else{
            debt_is_checkbox=false;
        }
        if (recur_is_checkbox.checked==true){
            recur_is_checkbox=true;
        } else{
            recur_is_checkbox=false;
        }

        proj_name_list.push(project_name);
        proj_est_cost_list.push(est_cost);
        proj_const_year_list.push(const_year);
        proj_category_list.push(category);
        proj_description_list.push(description);
        proj_priority_list.push(priority);
        proj_const_cost_list.push(const_cost);
        proj_est_year_list.push(est_year);
        debt_checkbox_list.push(debt_is_checkbox);
        recur_checkbox_list.push(recur_is_checkbox);

    };


    var data = new FormData();

    var json_proj_name_list = JSON.stringify(proj_name_list);
    var json_proj_est_cost_list = JSON.stringify(proj_est_cost_list);
    var json_proj_const_year_list = JSON.stringify(proj_const_year_list);
    var json_proj_category_list = JSON.stringify(proj_category_list);
    var json_proj_description_list = JSON.stringify(proj_description_list);
    var json_proj_priority_list = JSON.stringify(proj_priority_list);
    var json_proj_const_cost_list = JSON.stringify(proj_const_cost_list);
    var json_proj_est_year_list = JSON.stringify(proj_est_year_list);
    var json_debt_checkbox_list = JSON.stringify(debt_checkbox_list);
    var json_recur_checkbox_list = JSON.stringify(recur_checkbox_list);

    data.append("project_name_list",json_proj_name_list);
    data.append("project_est_cost_list",json_proj_est_cost_list);
    data.append("project_const_year_list",json_proj_const_year_list);
    data.append("project_category_list",json_proj_category_list);
    data.append("project_description_list",json_proj_description_list);
    data.append("project_priority_list",json_proj_priority_list);
    data.append("project_const_cost_list",json_proj_const_cost_list);
    data.append("facility_id", facility_id);
    data.append("latitude", latitude);
    data.append("longitude", longitude);
    data.append("project_est_year_list",json_proj_est_year_list);
    data.append("debt_checkbox_list",json_debt_checkbox_list);
    data.append("recur_checkbox_list",json_recur_checkbox_list);

    var save_updates_to_db = ajax_update_database_with_file("save-updates-to-db", data); //Submitting the data through the ajax function, see main.js for the helper function.
    save_updates_to_db.done(function(return_data){ //Reset the form once the data is added successfully
    });

    closeModal();

};
//function getAllofEm () {
//
//var allLayers = [];
//var map = TETHYS_MAP_VIEW.getMap();
//var mapLayers = map.getLayers().getArray();
//
//mapLayers.forEach(function (layer, i) {
//    if (layer instanceof ol.layer.Group && layer.getVisible() == true ) {
//        layer.getLayers().getArray().forEach(function(sublayer, j, layers) {
//            allLayers.push(sublayer);
//        })
//    } else if ( !(layer instanceof ol.layer.Group) && layer.getVisible() == true ) {
//            allLayers.push(layer);
//    }
//});
//
//return allLayers;
//}
//
//function needMeSomeLayers () {
//
//var layerArray = getAllofEm();
//
//  layerArray.forEach(layer, function() {
//
//    // do something with them
//  })
//}
//
//function getSomeLayers(id) {
//
//var map = TETHYS_MAP_VIEW.getMap();
//
//map.getLayers(id);
//}
function numToCurrency(number){
//    var currency = "$"+((number).toLocaleString('en'));
    number += '';
        var x = number.split('.');
        var x1 = x[0];
        var x2 = x.length > 1 ? '.' + x[1] : '';
        var rgx = /(\d+)(\d{3})/;
        while (rgx.test(x1)) {
                x1 = x1.replace(rgx, '$1' + ',' + '$2');
        }
    var currency = "$"+x1 + x2;


    return (currency)
};
function currencyToNumber(currency){
    var number = (currency.replace(/,/g,'')).replace('$','');
    return (number)
};

function inflationCheck(row_num){

        this_est_cost = parseFloat(document.getElementById(row_num+'-project-estcost').value)
        this_const_year = parseFloat(document.getElementById(row_num+'-project-constyear').value)
        this_est_year = parseFloat(document.getElementById(row_num+'-project-estyear').value)
        document.getElementById(row_num+'-project-constcost').value = ((this_est_cost*Math.pow(1.04,(this_const_year-this_est_year))).toFixed(0)).toString();

};
function inflationCheckC(row_num){

        this_est_cost = parseFloat(document.getElementById(row_num+'-projectc-estcost').value)
        this_const_year = parseFloat(document.getElementById(row_num+'-projectc-constyear').value)
        this_est_year = parseFloat(document.getElementById(row_num+'-projectc-estyear').value)
        document.getElementById(row_num+'-projectc-constcost').value = ((this_est_cost*Math.pow(1.04,(this_const_year-this_est_year))).toFixed(0)).toString();

};
function debtCheckboxCheck(row_num){



        if((document.getElementById(other).checked =="true")&&(other.checked ==true)){
            document.getElementById(other).checked = false;
        }
};
function saveCatDataToDB () {
    var location_list = document.getElementById('modal-category').value;
    var category = document.getElementById('modal-category').innerHTML;



    var proj_facility_id_list = []
    var proj_name_list = [];
    var proj_est_cost_list = [];
    var proj_const_year_list = [];
    var proj_category_list = [];
    var proj_description_list = [];
    var proj_priority_list = [];
    var proj_const_cost_list = [];
    var proj_est_year_list = [];
    var debt_checkbox_list = [];
    var recur_checkbox_list = [];

    var project_names = document.querySelectorAll('.projectc-name');

    for (var i = 1; i <= project_names.length; i++) {

        project_name = document.getElementById( i+'-projectc-name').value;
        est_cost = document.getElementById(i+'-projectc-estcost').value;
        est_cost = currencyToNumber(document.getElementById(i+'-projectc-estcost').value);

        const_year = document.getElementById(i+'-projectc-constyear').value;
        facility_id = document.getElementById(i+'-projectc-facilityid').value;
        description = document.getElementById(i+'-projectc-description').value;
        priority = document.getElementById(i+'-projectc-priority').value;
        const_cost = document.getElementById(i+'-projectc-constcost').value;
        const_cost = currencyToNumber(document.getElementById(i+'-projectc-constcost').value);

        est_year = document.getElementById(i+'-projectc-estyear').value;
        debt_is_checkbox = document.getElementById(i+'-debtc-checkbox');
        recur_is_checkbox = document.getElementById(i+'-recurc-checkbox');

        if (debt_is_checkbox.checked==true){
            debt_is_checkbox=true;
        } else{
            debt_is_checkbox=false;
        }
        if (recur_is_checkbox.checked==true){
            recur_is_checkbox=true;
        } else{
            recur_is_checkbox=false;
        }

        proj_facility_id_list.push(facility_id);
        proj_name_list.push(project_name);
        proj_est_cost_list.push(est_cost);
        proj_const_year_list.push(const_year);
        proj_category_list.push(category);
        proj_description_list.push(description);
        proj_priority_list.push(priority);
        proj_const_cost_list.push(const_cost);
        proj_est_year_list.push(est_year);
        debt_checkbox_list.push(debt_is_checkbox);
        recur_checkbox_list.push(recur_is_checkbox);

    };


    var data = new FormData();

    var json_location_list = JSON.stringify(location_list);
    var json_proj_name_list = JSON.stringify(proj_name_list);
    var json_proj_est_cost_list = JSON.stringify(proj_est_cost_list);
    var json_proj_const_year_list = JSON.stringify(proj_const_year_list);
    var json_proj_facility_id_list = JSON.stringify(proj_facility_id_list);
    var json_proj_description_list = JSON.stringify(proj_description_list);
    var json_proj_priority_list = JSON.stringify(proj_priority_list);
    var json_proj_const_cost_list = JSON.stringify(proj_const_cost_list);
    var json_proj_est_year_list = JSON.stringify(proj_est_year_list);
    var json_debt_checkbox_list = JSON.stringify(debt_checkbox_list);
    var json_recur_checkbox_list = JSON.stringify(recur_checkbox_list);

    data.append('location_list', json_location_list);
    data.append("project_name_list",json_proj_name_list);
    data.append("project_est_cost_list",json_proj_est_cost_list);
    data.append("project_const_year_list",json_proj_const_year_list);
    data.append("project_facility_id_list",json_proj_facility_id_list);
    data.append("project_description_list",json_proj_description_list);
    data.append("project_priority_list",json_proj_priority_list);
    data.append("project_const_cost_list",json_proj_const_cost_list);
    data.append("category", category);
    data.append("project_est_year_list",json_proj_est_year_list);
    data.append("debt_checkbox_list",json_debt_checkbox_list);
    data.append("recur_checkbox_list",json_recur_checkbox_list);

    var save_cat_updates_to_db = ajax_update_database_with_file("save-cat-updates-to-db", data); //Submitting the data through the ajax function, see main.js for the helper function.
    save_cat_updates_to_db.done(function(return_data){




     //Reset the form once the data is added successfully
    });

    closeModal();

};

function swModal(){
    // Get the Open Layers map object from the Tethys MapView
    var map = TETHYS_MAP_VIEW.getMap();

    $("#map-bottom-modal").modal('show');
    document.getElementById('modal-category').innerHTML = "Stormwater";

    var data = new FormData();
    data.append("category","Stormwater");

    var get_project_categorized_list = ajax_update_database_with_file("get-project-categorized-list", data); //Submitting the data through the ajax function, see main.js for the helper function.
    get_project_categorized_list.done(function(return_data){
        updateCategorizedModal(return_data);
    });
}

function wwModal(){
    // Get the Open Layers map object from the Tethys MapView
    var map = TETHYS_MAP_VIEW.getMap();

    $("#map-bottom-modal").modal('show');
    document.getElementById('modal-category').innerHTML = "Wastewater";

    var data = new FormData();
    data.append("category","Wastewater");

    var get_project_categorized_list = ajax_update_database_with_file("get-project-categorized-list", data); //Submitting the data through the ajax function, see main.js for the helper function.
    get_project_categorized_list.done(function(return_data){
        updateCategorizedModal(return_data);
    });
}


function wModal(){
    // Get the Open Layers map object from the Tethys MapView
    var map = TETHYS_MAP_VIEW.getMap();

    $("#map-bottom-modal").modal('show');
    document.getElementById('modal-category').innerHTML = "Water";

    var data = new FormData();
    data.append("category","Water");

    var get_project_categorized_list = ajax_update_database_with_file("get-project-categorized-list", data); //Submitting the data through the ajax function, see main.js for the helper function.
    get_project_categorized_list.done(function(return_data){
        updateCategorizedModal(return_data);
    });
}


function transpoModal(){
    // Get the Open Layers map object from the Tethys MapView
    var map = TETHYS_MAP_VIEW.getMap();

    $("#map-bottom-modal").modal('show');
    document.getElementById('modal-category').innerHTML = "Transportation";

    var data = new FormData();
    data.append("category","Transportation");

    var get_project_categorized_list = ajax_update_database_with_file("get-project-categorized-list", data); //Submitting the data through the ajax function, see main.js for the helper function.
    get_project_categorized_list.done(function(return_data){
        updateCategorizedModal(return_data);
    });
}


function golfModal(){
    // Get the Open Layers map object from the Tethys MapView
    var map = TETHYS_MAP_VIEW.getMap();

    $("#map-bottom-modal").modal('show');
    document.getElementById('modal-category').innerHTML = "Golf";

    var data = new FormData();
    data.append("category","Golf");

    var get_project_categorized_list = ajax_update_database_with_file("get-project-categorized-list", data); //Submitting the data through the ajax function, see main.js for the helper function.
    get_project_categorized_list.done(function(return_data){
        updateCategorizedModal(return_data);
    });
}


function facilitiesModal(){
    // Get the Open Layers map object from the Tethys MapView
    var map = TETHYS_MAP_VIEW.getMap();

    $("#map-bottom-modal").modal('show');
    document.getElementById('modal-category').innerHTML = "Facilities";

    var data = new FormData();
    data.append("category","Facilities");

    var get_project_categorized_list = ajax_update_database_with_file("get-project-categorized-list", data); //Submitting the data through the ajax function, see main.js for the helper function.
    get_project_categorized_list.done(function(return_data){
        updateCategorizedModal(return_data);
    });
}

function financialModal(){
    // Get the Open Layers map object from the Tethys MapView
    var map = TETHYS_MAP_VIEW.getMap();

    $("#map-bottom-modal").modal('show');
    document.getElementById('modal-category').innerHTML = "Existing Debt";

    var data = new FormData();
    data.append("category","Existing Debt");

    var get_project_categorized_list = ajax_update_database_with_file("get-project-categorized-list", data); //Submitting the data through the ajax function, see main.js for the helper function.
    get_project_categorized_list.done(function(return_data){
        updateCategorizedModal(return_data);
    });
}

function updateCategorizedModal(return_data){
    if("lat_list" in return_data){
        lat_list = return_data.lat_list;
    };
    if("lon_list" in return_data){
        lon_list = return_data.lon_list;
    };
    if("facility_id" in return_data){
        project_facility_id_list = return_data.facility_id;
    };

    if("est_year" in return_data){
        project_est_year_list = return_data.est_year;
    };

    if("project_name" in return_data){
        project_name_list = return_data.project_name;
    };

    if("est_cost" in return_data){
        project_est_cost_list = return_data.est_cost;
    };

    if("const_year" in return_data){
        project_const_year_list = return_data.const_year;
    };

    if("description" in return_data){
        project_description_list = return_data.description;
    };

    if("priority" in return_data){
        project_priority_list = return_data.priority;
    };

    if("const_cost" in return_data){
        project_const_cost_list = return_data.const_cost;
    };

    if("debt_checkbox" in return_data){
        debt_checkbox_list = return_data.debt_checkbox;
        console.log(return_data.debt_checkbox);

    };
    if("recur_checkbox" in return_data){
        recur_checkbox_list = return_data.recur_checkbox;
        console.log(return_data.recur_checkbox);

    };

    $('#project-list-table-2 tr').not(':first').remove();
    var html = '';
    location_list = [JSON.stringify(lat_list), JSON.stringify(lon_list)];
    document.getElementById('modal-category').value = location_list;
    for(var i = 0; i < project_name_list.length; i++){
        if(debt_checkbox_list[i] == "true"){
            console.log("truth revealed")
            debt_is_checked = " checked ";
        } else{
            debt_is_checked = " ";
        }
        if(recur_checkbox_list[i] == "true"){
            recur_is_checked = " checked ";
        } else{
            recur_is_checked = " ";
        }
        console.log(project_const_cost_list)

        html += '<tr id="row-'+(i+1)+'">'+
                    '<td><input class="cedit-fields" type="text" id="' + (i+1) +'-projectc-facilityid" value="'+ project_facility_id_list[i] + '" disabled></td>' +
                    '<td><input class="cedit-fields projectc-name" type="text" id="' + (i+1) +'-projectc-name" value="'+ project_name_list[i] + '" disabled></td>' +
                    '<td><input class="cedit-fields" type="text" id="' + (i+1) +'-projectc-priority" value="'+ project_priority_list[i] + '" disabled></td>' +
                    '<td><input class="cedit-fields" type="text" id="' + (i+1) +'-projectc-description" value="'+ project_description_list[i] + '" disabled></td>' +
                    '<td><input class="cedit-fields" type="text" onchange="inflationCheckC('+(i+1)+');" id="' + (i+1) +'-projectc-estyear" value="'+ project_est_year_list[i] + '" disabled></td>' +
                    '<td><input class="cedit-fields" type="text" onchange="inflationCheckC('+(i+1)+');" id="' + (i+1) +'-projectc-estcost" value="'+ numToCurrency(project_est_cost_list[i]) + '" disabled></td>' +
                    '<td><input class="cedit-fields" type="text" onchange="inflationCheckC('+(i+1)+');" id="' + (i+1) +'-projectc-constyear" value="'+ project_const_year_list[i] + '" disabled></td>' +
                    '<td><input class="cedit-fields" type="text" id="' + (i+1) +'-projectc-constcost" value="'+ numToCurrency(project_const_cost_list[i]) + '" disabled></td>' +
                    '<td><input class="cedit-fields" type="checkbox" id="' + (i+1) +'-debtc-checkbox"'+ debt_is_checked + 'disabled></td>' +
                    '<td><input class="cedit-fields" type="checkbox" id="' + (i+1) +'-recurc-checkbox"'+ recur_is_checked + 'disabled></td>' +
                    '<td class="table-button"><div"><a name="csubmit-stop-edit-region" style="display:none;" id="cstop-edit-button-'+(i+1)+'" onclick="stopCatEditRow('+(i+1)+');" class="btn btn-success csubmit-stop-edit-region" role="button">'+
                    '<span class="glyphicon glyphicon-save"></span></a><a name="csubmit-edit-region" id="cedit-button-'+(i+1)+'" onclick="editCatRow('+(i+1)+');" class="btn btn-warning csubmit-edit-region" role="button">'+
                    '<span class="glyphicon glyphicon-edit"></span></a><a name="csubmit-delete-region" id="cdelete-button-'+(i+1)+'" onclick="deleteCatRow(this);" class="btn btn-danger csubmit-delete-region" role="button">'+
                    '<span class="glyphicon glyphicon-remove"></span></a>'+
                    '</div>'+
                    '</td>'+
                '</tr>';
    };

    $('#project-list-table-2 tr').first().after(html);
     //Reset the form once the data is added successfully
}


function editCatRow (row_num){
    console.log("In edit row")

    document.getElementById('cstop-edit-button-'+row_num).style.display = 'inline-block';
    document.getElementById('cdelete-button-'+row_num).disabled = true;

    var delete_buttons = document.querySelectorAll('.csubmit-delete-region');
    var edit_buttons = document.querySelectorAll('.csubmit-edit-region');

    for (var i = 0; i < delete_buttons.length; i++) {
        delete_buttons[i].style.backgroundColor = "gray";
        delete_buttons[i].style.borderColor = "#000000";
    };
    for (var j = 0; j < edit_buttons.length; j++){
        edit_buttons[j].style.display = 'none';

    };
    document.getElementById(row_num+'-projectc-name').disabled = false;
    document.getElementById(row_num+'-projectc-name').style.border = '1px solid';

    document.getElementById(row_num+'-projectc-estcost').disabled = false;
    document.getElementById(row_num+'-projectc-estcost').style.border = '1px solid';
    document.getElementById(row_num+'-projectc-estcost').value = currencyToNumber(document.getElementById(row_num+'-projectc-estcost').value);


    document.getElementById(row_num+'-projectc-constyear').disabled = false;
    document.getElementById(row_num+'-projectc-constyear').style.border = '1px solid';

    document.getElementById(row_num+'-projectc-facilityid').disabled = false;
    document.getElementById(row_num+'-projectc-facilityid').style.border = '1px solid';

    document.getElementById(row_num+'-projectc-description').disabled = false;
    document.getElementById(row_num+'-projectc-description').style.border = '1px solid';

    document.getElementById(row_num+'-projectc-priority').disabled = false;
    document.getElementById(row_num+'-projectc-priority').style.border = '1px solid';

    document.getElementById(row_num+'-projectc-estyear').disabled = false;
    document.getElementById(row_num+'-projectc-estyear').style.border = '1px solid';

    document.getElementById(row_num+'-projectc-constcost').disabled = false;
    document.getElementById(row_num+'-projectc-constcost').style.border = '1px solid';
    document.getElementById(row_num+'-projectc-constcost').value = currencyToNumber(document.getElementById(row_num+'-projectc-constcost').value);

    document.getElementById(row_num+'-debtc-checkbox').disabled = false;
    document.getElementById(row_num+'-debtc-checkbox').style.border = '1px solid';

    document.getElementById(row_num+'-recurc-checkbox').disabled = false;
    document.getElementById(row_num+'-recurc-checkbox').style.border = '1px solid';

    $('#'+row_num+'-projectc-estyear').change(function(){
        this_est_cost = parseFloat(document.getElementById(row_num+'-projectc-estcost').value)
        this_const_year = parseFloat(document.getElementById(row_num+'-projectc-constyear').value)
        this_est_year = parseFloat(document.getElementById(row_num+'-projectc-estyear').value)
        document.getElementById(row_num+'-projectc-constcost').value = ((this_est_cost*Math.pow(1.04,(this_const_year-this_est_year))).toFixed(0)).toString();
    });
    $('#'+row_num+'-projectc-estcost').change(function(){
        this_est_cost = parseFloat(document.getElementById(row_num+'-projectc-estcost').value)
        this_const_year = parseFloat(document.getElementById(row_num+'-projectc-constyear').value)
        this_est_year = parseFloat(document.getElementById(row_num+'-projectc-estyear').value)
        document.getElementById(row_num+'-projectc-constcost').value = ((this_est_cost*Math.pow(1.04,(this_const_year-this_est_year))).toFixed(0)).toString();
    });
    $('#'+row_num+'-projectc-constyear').change(function(){
        this_est_cost = parseFloat(document.getElementById(row_num+'-projectc-estcost').value)
        this_const_year = parseFloat(document.getElementById(row_num+'-projectc-constyear').value)
        this_est_year = parseFloat(document.getElementById(row_num+'-projectc-estyear').value)
        document.getElementById(row_num+'-projectc-constcost').value = ((this_est_cost*Math.pow(1.04,(this_const_year-this_est_year))).toFixed(0)).toString();
    });

    $('#'+row_num+'-debtc-checkbox').change(function(){
        if(document.getElementById(row_num+'-debtc-checkbox').value =="on"){
            document.getElementById(row_num+'-recurc-checkbox').checked = false;
        }
    });
    $('#'+row_num+'-recurc-checkbox').change(function(){
        if(document.getElementById(row_num+'-recurc-checkbox').value == "on"){
            document.getElementById(row_num+'-debtc-checkbox').checked = false;
        }
    });

};

function stopCatEditRow (row_num){

    document.getElementById('cstop-edit-button-'+row_num).style.display = 'none';
    document.getElementById('cdelete-button-'+row_num).disabled = false;

    var delete_buttons = document.querySelectorAll('.csubmit-delete-region');
    var edit_buttons = document.querySelectorAll('.csubmit-edit-region');


    for (var i = 0; i < delete_buttons.length; i++) {
        delete_buttons[i].style.backgroundColor = "#d9534f";
        delete_buttons[i].style.borderColor = "#d43f3a";
    };
    for (var j = 0; j < edit_buttons.length; j++){
        edit_buttons[j].style.display = 'inline-block';

    };
    document.getElementById(row_num+'-projectc-name').disabled = true;
    document.getElementById(row_num+'-projectc-name').style.border = 'none';

    document.getElementById(row_num+'-projectc-estcost').disabled = true;
    document.getElementById(row_num+'-projectc-estcost').style.border = 'none';
    document.getElementById(row_num+'-projectc-estcost').value = numToCurrency(document.getElementById(row_num+'-projectc-estcost').value);

    document.getElementById(row_num+'-projectc-constyear').disabled = true;
    document.getElementById(row_num+'-projectc-constyear').style.border = 'none';

    document.getElementById(row_num+'-projectc-facilityid').disabled = true;
    document.getElementById(row_num+'-projectc-facilityid').style.border = 'none';

    document.getElementById(row_num+'-projectc-description').disabled = true;
    document.getElementById(row_num+'-projectc-description').style.border = 'none';

    document.getElementById(row_num+'-projectc-priority').disabled = true;
    document.getElementById(row_num+'-projectc-priority').style.border = 'none';

    document.getElementById(row_num+'-projectc-estyear').disabled = true;
    document.getElementById(row_num+'-projectc-estyear').style.border = 'none';

    document.getElementById(row_num+'-projectc-constcost').disabled = true;
    document.getElementById(row_num+'-projectc-constcost').style.border = 'none';
    document.getElementById(row_num+'-projectc-constcost').value = numToCurrency(document.getElementById(row_num+'-projectc-constcost').value);

    document.getElementById(row_num+'-debtc-checkbox').disabled = true;
    document.getElementById(row_num+'-debtc-checkbox').style.border = 'none';

    document.getElementById(row_num+'-recurc-checkbox').disabled = true;
    document.getElementById(row_num+'-recurc-checkbox').style.border = 'none';
};

function deleteProjRow (elem){
    console.log(parseInt((elem.id).slice((elem.id).lastIndexOf("-")-(elem.id).length+1)));
    row_num = parseInt((elem.id).slice((elem.id).lastIndexOf("-")-(elem.id).length+1));
    document.getElementById("project-list-table").deleteRow(row_num);

    var project_names = document.querySelectorAll('.project-name');

    for (var i=row_num+1; i<=project_names.length+1; i++){
        document.getElementById(i+'-project-name').id = (i-1)+'-project-name';
        document.getElementById(i+'-project-estcost').id = (i-1)+'-project-estcost';
        document.getElementById(i+'-project-constyear').id =  (i-1)+'-project-constyear';
        document.getElementById(i+'-project-category').id = (i-1)+'-project-category';
        document.getElementById(i+'-project-description').id = (i-1)+'-project-description';
        document.getElementById(i+'-project-priority').id =(i-1)+'-project-priority';
        document.getElementById(i+'-project-estyear').id = (i-1)+'-project-estyear';
        document.getElementById(i+'-project-constcost').id =(i-1)+'-project-constcost';
        document.getElementById(i+'-debt-checkbox').id =(i-1)+'-debt-checkbox';
        document.getElementById(i+'-recur-checkbox').id =(i-1)+'-recur-checkbox';
        document.getElementById('stop-edit-button-'+i).id ='stop-edit-button-'+(i-1);
        document.getElementById('edit-button-'+i).id ='edit-button-'+(i-1);
        document.getElementById('delete-button-'+i).id ='delete-button-'+(i-1);
    }
};

function deleteCatRow (elem){


    var new_row_num = parseInt((elem.id).slice((elem.id).lastIndexOf("-")-(elem.id).length+1));
    console.log(new_row_num)
    var project_names = document.querySelectorAll('.projectc-name');
    document.getElementById("project-list-table-2").deleteRow(new_row_num);

    for (var i=new_row_num+1; i<=project_names.length; i++){
        document.getElementById(i+'-projectc-name').id = (i-1)+'-projectc-name';
        document.getElementById(i+'-projectc-estcost').id = (i-1)+'-projectc-estcost';
        document.getElementById(i+'-projectc-constyear').id =  (i-1)+'-projectc-constyear';
        document.getElementById(i+'-projectc-facilityid').id = (i-1)+'-projectc-facilityid';
        document.getElementById(i+'-projectc-description').id = (i-1)+'-projectc-description';
        document.getElementById(i+'-projectc-priority').id =(i-1)+'-projectc-priority';
        document.getElementById(i+'-projectc-estyear').id = (i-1)+'-projectc-estyear';
        document.getElementById(i+'-projectc-constcost').id =(i-1)+'-projectc-constcost';
        document.getElementById(i+'-debtc-checkbox').id =(i-1)+'-debtc-checkbox';
        document.getElementById(i+'-recurc-checkbox').id =(i-1)+'-recurc-checkbox';
        document.getElementById('cstop-edit-button-'+i).id ='cstop-edit-button-'+(i-1);
        document.getElementById('cedit-button-'+i).id ='cedit-button-'+(i-1);
        document.getElementById('cdelete-button-'+i).id ='cdelete-button-'+(i-1);
    }
};

function addCatProjectRow (){
    console.log("In Cat Add Project Row")

    var html = '';

        var nrows = document.querySelectorAll('.projectc-name');
        numrows = nrows.length;
        console.log(numrows);
        i = numrows;

        html += '<tr id="row-'+(i+1)+'">'+
                    '<td><input style="border: 1px solid" class="cedit-fields" type="text" id="' + (i+1) +'-projectc-facilityid" value="" ></td>' +
                    '<td><input style="border: 1px solid" class="cedit-fields projectc-name" type="text" id="' + (i+1) +'-projectc-name" value="" ></td>' +
                    '<td><input style="border: 1px solid" class="cedit-fields" type="text" id="' + (i+1) +'-projectc-priority" value="" ></td>' +
                    '<td><input style="border: 1px solid" class="cedit-fields" type="text" id="' + (i+1) +'-projectc-description" value="" ></td>' +
                    '<td><input style="border: 1px solid" class="cedit-fields" onchange="inflationCheckC('+(i+1)+');" type="text" id="' + (i+1) +'-projectc-estyear" value="" ></td>' +
                    '<td><input style="border: 1px solid" class="cedit-fields" onchange="inflationCheckC('+(i+1)+');" type="text" id="' + (i+1) +'-projectc-estcost" value="" ></td>' +
                    '<td><input style="border: 1px solid" class="cedit-fields" onchange="inflationCheckC('+(i+1)+');" type="text" id="' + (i+1) +'-projectc-constyear" value="" ></td>' +
                    '<td><input style="border: 1px solid" class="cedit-fields" type="text" id="' + (i+1) +'-projectc-constcost" value="" ></td>' +
                    '<td><input class="cedit-fields" type="checkbox" id="' + (i+1) +'-debtc-checkbox" value="true"></td>' +
                    '<td><input class="cedit-fields" type="checkbox" id="' + (i+1) +'-recurc-checkbox" value="true"></td>' +
                    '<td class="table-button"><div"><a name="csubmit-stop-edit-region" style="display:none;" id="cstop-edit-button-'+(i+1)+'" onclick="stopCatEditRow('+(i+1)+');" class="btn btn-success csubmit-stop-edit-region" role="button">'+
                    '<span class="glyphicon glyphicon-save"></span>  </a><a name="csubmit-edit-region" id="cedit-button-'+(i+1)+'" onclick="editCatRow('+(i+1)+');" class="btn btn-warning csubmit-edit-region" role="button">'+
                    '<span class="glyphicon glyphicon-edit"></span>  </a><a name="csubmit-delete-region" id="cdelete-button-'+(i+1)+'" onclick="deleteCatRow(this);" class="btn btn-danger csubmit-delete-region" role="button">'+
                    '<span class="glyphicon glyphicon-remove"></span>  </a>'+
                    '</div>'+
                    '</td>'+
                '</tr>';


    $('#project-list-table-2 tr').last().after(html);

    html2 = "Projects added in this window will not appear on the map. Projects must be added on the 'Add Project' page to be seen on the map. Do you wish to continue?";
    document.getElementById('warning-message').innerText = html2;

    editCatRow(i+1);

    $("#submodal-modal").modal('show');
};
//function checkboxCheck(row_num, elem){
//        console.log(elem);
//        if (elem == document.getElementById(row_num+'-debt-checkbox'))
//        {
//            othercheck = document.getElementById(row_num+'-recur-checkbox')
//        }
//        else (elem == document.getElementById(row_num+'-recur-checkbox'))
//        {
//            othercheck = document.getElementById(row_num+'-debt-checkbox')
//        }
//
//       if ((elem).checked == true)
//       {
//            othercheck.checked = false
//       }
//       if ((othercheck).checked == true)
//       {
//            elem.checked = false
//       }
//        if(document.getElementById(row_num+'-debt-checkbox').checked ==true){
//            document.getElementById(row_num+'-recur-checkbox').checked = false;
//        }
//};


$(function() {

    // Get the Open Layers map object from the Tethys MapView
    var map = TETHYS_MAP_VIEW.getMap();
    var layer_list = map.getLayers();
    console.log(layer_list);
    // Get the Select Interaction from the Tethys MapView
    var select_interaction = TETHYS_MAP_VIEW.getSelectInteraction();

    // When selected, call function to display properties
    select_interaction.getFeatures().on('change:length', function(e)
    {
        if (e.target.getArray().length > 0)
        {
            $("#map-popup-modal").modal('show');
            // this means there is at least 1 feature selected
            var selected_feature = e.target.item(0); // 1st feature in Collection

            // Get coordinates of the point to set position of the popup
            var coordinates = selected_feature.getGeometry().getCoordinates();

            document.getElementById('modal-facility-id').innerHTML = "Facility ID: "+ selected_feature.get('facility_id');


            var data = new FormData();
            data.append("facility_id",selected_feature.get('facility_id'));
            data.append("coordinates",selected_feature.getGeometry().getCoordinates());


            var get_project_list = ajax_update_database_with_file("get-project-list", data); //Submitting the data through the ajax function, see main.js for the helper function.
            get_project_list.done(function(return_data){

                if("lat" in return_data){
                    lat = return_data.lat;
                };
                if("lon" in return_data){
                    lon = return_data.lon;
                };
                if("est_year" in return_data){
                    project_est_year_list = return_data.est_year;
                };

                if("project_name" in return_data){
                    project_name_list = return_data.project_name;
                };

                if("est_cost" in return_data){
                    project_est_cost_list = return_data.est_cost;
                };

                if("const_year" in return_data){
                    project_const_year_list = return_data.const_year;
                };

                if("category" in return_data){
                    project_category_list = return_data.category;
                };

                if("description" in return_data){
                    project_description_list = return_data.description;
                };

                if("priority" in return_data){
                    project_priority_list = return_data.priority;
                };

                if("const_cost" in return_data){
                    project_const_cost_list = return_data.const_cost;
                };

                if("debt_checkbox" in return_data){
                    debt_checkbox_list = return_data.debt_checkbox;
                    console.log(return_data.debt_checkbox);

                };
                if("recur_checkbox" in return_data){
                    recur_checkbox_list = return_data.recur_checkbox;
                    console.log(return_data.recur_checkbox);

                };
                document.getElementById('modal-facility-id').value = [lat,lon]
                $('#project-list-table tr').not(':first').remove();
                var html = '';

                for(var i = 0; i < project_name_list.length; i++){
                    if(debt_checkbox_list[i] == "true"){
                        console.log("truth revealed")
                        debt_is_checked = " checked ";
                    } else{
                        debt_is_checked = " ";
                    }
                    if(recur_checkbox_list[i] == "true"){
                        recur_is_checked = " checked ";
                    } else{
                        recur_is_checked = " ";
                    }

                    console.log(project_const_cost_list)

                    html += '<tr id="row-'+(i+1)+'">'+
                                '<td><input class="edit-fields project-name" type="text" id="' + (i+1) +'-project-name" value="'+ project_name_list[i] + '" disabled></td>' +
                                '<td><input class="edit-fields" type="text" id="' + (i+1) +'-project-category" value="'+ project_category_list[i] + '" disabled></td>' +
                                '<td><input class="edit-fields" type="text" id="' + (i+1) +'-project-priority" value="'+ project_priority_list[i] + '" disabled></td>' +
                                '<td><input class="edit-fields" type="text" id="' + (i+1) +'-project-description" value="'+ project_description_list[i] + '" disabled></td>' +
                                '<td><input class="edit-fields" type="text" onchange="inflationCheck('+(i+1)+');" id="' + (i+1) +'-project-estyear" value="'+ project_est_year_list[i] + '" disabled></td>' +
                                '<td><input class="edit-fields" type="text" onchange="inflationCheck('+(i+1)+');" id="' + (i+1) +'-project-estcost" value="'+ numToCurrency(project_est_cost_list[i]) + '" disabled></td>' +
                                '<td><input class="edit-fields" type="text" onchange="inflationCheck('+(i+1)+');" id="' + (i+1) +'-project-constyear" value="'+ project_const_year_list[i] + '" disabled></td>' +
                                '<td><input class="edit-fields" type="text" id="' + (i+1) +'-project-constcost" value="'+ numToCurrency(project_const_cost_list[i]) + '" disabled></td>' +
                                '<td><input class="edit-fields" type="checkbox" id="' + (i+1) +'-debt-checkbox"'+ debt_is_checked + 'disabled></td>' +
                                '<td><input class="edit-fields" type="checkbox" id="' + (i+1) +'-recur-checkbox"'+ recur_is_checked + 'disabled></td>' +
                                '<td class="table-button"><div style:"white-space: nowrap;"><a name="submit-stop-edit-region" style="display:none;" aria-label="Stop Editing" id="stop-edit-button-'+(i+1)+'" onclick="stopEditRow('+(i+1)+');" class="btn btn-group btn-success submit-stop-edit-region" role="button">'+
                                '<span class="glyphicon glyphicon-save"></span></a><a name="submit-edit-region" aria-label="Edit Row" id="edit-button-'+(i+1)+'" onclick="editRow('+(i+1)+');" class="btn btn-group btn-warning submit-edit-region" role="button">'+
                                '<span class="glyphicon glyphicon-edit"></span></a><a name="submit-delete-region" aria-label="Delete Row" onclick="deleteProjRow(this);" id="delete-button-'+(i+1)+'" class="btn btn-danger button-group submit-delete-region" role="button">'+
                                '<span class="glyphicon glyphicon-remove"></span></a>'+
                                '</div>'+
                                '</td>'+
                            '</tr>';
                };

                $('#project-list-table tr').first().after(html);
                 //Reset the form once the data is added successfully
            });

        } else {}
    });
});
function closeModal (){
    var map = TETHYS_MAP_VIEW.getMap();

    // Get the Select Interaction from the Tethys MapView
    var select_interaction = TETHYS_MAP_VIEW.getSelectInteraction();

    select_interaction.getFeatures().clear();
};

function editRow (row_num){

    document.getElementById('stop-edit-button-'+row_num).style.display = 'inline-block';
    document.getElementById('delete-button-'+row_num).disabled = true;

    var delete_buttons = document.querySelectorAll('.submit-delete-region');
    var edit_buttons = document.querySelectorAll('.submit-edit-region');


    for (var i = 0; i < delete_buttons.length; i++) {
        delete_buttons[i].style.backgroundColor = "gray";
        delete_buttons[i].style.borderColor = "#000000";
    };
    for (var j = 0; j < edit_buttons.length; j++){
        edit_buttons[j].style.display = 'none';

    };
    document.getElementById(row_num+'-project-name').disabled = false;
    document.getElementById(row_num+'-project-name').style.border = '1px solid';

    document.getElementById(row_num+'-project-estcost').disabled = false;
    document.getElementById(row_num+'-project-estcost').style.border = '1px solid';
    document.getElementById(row_num+'-project-estcost').value = currencyToNumber(document.getElementById(row_num+'-project-estcost').value);

    document.getElementById(row_num+'-project-constyear').disabled = false;
    document.getElementById(row_num+'-project-constyear').style.border = '1px solid';

    document.getElementById(row_num+'-project-category').disabled = false;
    document.getElementById(row_num+'-project-category').style.border = '1px solid';

    document.getElementById(row_num+'-project-description').disabled = false;
    document.getElementById(row_num+'-project-description').style.border = '1px solid';

    document.getElementById(row_num+'-project-priority').disabled = false;
    document.getElementById(row_num+'-project-priority').style.border = '1px solid';

    document.getElementById(row_num+'-project-estyear').disabled = false;
    document.getElementById(row_num+'-project-estyear').style.border = '1px solid';

    document.getElementById(row_num+'-project-constcost').disabled = false;
    document.getElementById(row_num+'-project-constcost').style.border = '1px solid';
    document.getElementById(row_num+'-project-constcost').value = currencyToNumber(document.getElementById(row_num+'-project-constcost').value);

    document.getElementById(row_num+'-debt-checkbox').disabled = false;
    document.getElementById(row_num+'-debt-checkbox').style.border = '1px solid';

    document.getElementById(row_num+'-recur-checkbox').disabled = false;
    document.getElementById(row_num+'-recur-checkbox').style.border = '1px solid';



};

function stopEditRow (row_num){

    document.getElementById('stop-edit-button-'+row_num).style.display = 'none';
    document.getElementById('delete-button-'+row_num).disabled = false;

    var delete_buttons = document.querySelectorAll('.submit-delete-region');
    var edit_buttons = document.querySelectorAll('.submit-edit-region');


    for (var i = 0; i < delete_buttons.length; i++) {
        delete_buttons[i].style.backgroundColor = "#d9534f";
        delete_buttons[i].style.borderColor = "#d43f3a";
    };
    for (var j = 0; j < edit_buttons.length; j++){
        edit_buttons[j].style.display = 'inline-block';

    };
    document.getElementById(row_num+'-project-name').disabled = true;
    document.getElementById(row_num+'-project-name').style.border = 'none';

    document.getElementById(row_num+'-project-estcost').disabled = true;
    document.getElementById(row_num+'-project-estcost').style.border = 'none';
    document.getElementById(row_num+'-project-estcost').value = numToCurrency(document.getElementById(row_num+'-project-estcost').value);


    document.getElementById(row_num+'-project-constyear').disabled = true;
    document.getElementById(row_num+'-project-constyear').style.border = 'none';

    document.getElementById(row_num+'-project-category').disabled = true;
    document.getElementById(row_num+'-project-category').style.border = 'none';

    document.getElementById(row_num+'-project-description').disabled = true;
    document.getElementById(row_num+'-project-description').style.border = 'none';

    document.getElementById(row_num+'-project-priority').disabled = true;
    document.getElementById(row_num+'-project-priority').style.border = 'none';

    document.getElementById(row_num+'-project-estyear').disabled = true;
    document.getElementById(row_num+'-project-estyear').style.border = 'none';

    document.getElementById(row_num+'-project-constcost').disabled = true;
    document.getElementById(row_num+'-project-constcost').style.border = 'none';
    document.getElementById(row_num+'-project-constcost').value = numToCurrency(document.getElementById(row_num+'-project-constcost').value);

    document.getElementById(row_num+'-debt-checkbox').disabled = true;
    document.getElementById(row_num+'-debt-checkbox').style.border = 'none';

    document.getElementById(row_num+'-recur-checkbox').disabled = true;
    document.getElementById(row_num+'-recur-checkbox').style.border = 'none';
};

function addProjectRow (){
    console.log("In Add Project Row")

    var html = '';

        var nrows = document.querySelectorAll('.project-name');
        numrows = nrows.length;
        console.log(numrows);
        i = numrows;

        html += '<tr id="row-'+(i+1)+'">'+
                    '<td><input style="border: 1px solid" class="edit-fields project-name" type="text" id="' + (i+1) +'-project-name" value="" ></td>' +
                    '<td><input style="border: 1px solid" class="edit-fields" type="text" id="' + (i+1) +'-project-category" value="" ></td>' +
                    '<td><input style="border: 1px solid" class="edit-fields" type="text" id="' + (i+1) +'-project-priority" value="" ></td>' +
                    '<td><input style="border: 1px solid" class="edit-fields" type="text" id="' + (i+1) +'-project-description" value="" ></td>' +
                    '<td><input style="border: 1px solid" class="edit-fields" onchange="inflationCheck('+(i+1)+')"; type="text" id="' + (i+1) +'-project-estyear" value="" ></td>' +
                    '<td><input style="border: 1px solid" class="edit-fields" onchange="inflationCheck('+(i+1)+')"; type="text" id="' + (i+1) +'-project-estcost" value="" ></td>' +
                    '<td><input style="border: 1px solid" class="edit-fields" onchange="inflationCheck('+(i+1)+')"; type="text" id="' + (i+1) +'-project-constyear" value="" ></td>' +
                    '<td><input style="border: 1px solid" class="edit-fields" type="text" id="' + (i+1) +'-project-constcost" value="" ></td>' +
                    '<td><input class="edit-fields" type="checkbox" id="' + (i+1) +'-debt-checkbox" value="true"></td>' +
                    '<td><input class="edit-fields" type="checkbox" id="' + (i+1) +'-recur-checkbox" value="true"></td>' +
                    '<td class="table-button"><div"><a name="submit-stop-edit-region" style="display:none;" id="stop-edit-button-'+(i+1)+'" onclick="stopEditRow('+(i+1)+');" class="btn btn-success submit-stop-edit-region" role="button">'+
                    '<span class="glyphicon glyphicon-save"></span></a><a name="submit-edit-region" id="edit-button-'+(i+1)+'" onclick="editRow('+(i+1)+');" class="btn btn-warning submit-edit-region" role="button">'+
                    '<span class="glyphicon glyphicon-edit"></span></a><a name="submit-delete-region" id="delete-button-'+(i+1)+'" onclick="deleteProjRow(this);" class="btn btn-danger submit-delete-region" role="button">'+
                    '<span class="glyphicon glyphicon-remove"></span></a>'+
                    '</div>'+
                    '</td>'+
                '</tr>';


    $('#project-list-table tr').last().after(html);
    editRow(i+1);
};
