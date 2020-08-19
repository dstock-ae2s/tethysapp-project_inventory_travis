function saveDataToDB () {
    console.log("In the JS")

    var facility_id = document.getElementById('modal-facility-id').innerHTML

    var proj_name_list = [];
    var proj_cost_list = [];
    var proj_year_list = [];

    var project_names = document.querySelectorAll('.project-name');

    for (var i = 1; i <= project_names.length; i++) {

        project_name = document.getElementById( i+'-project-name').value;
        cost = document.getElementById(i+'-project-cost').value;
        planned_year = document.getElementById(i+'-project-year').value;

        proj_name_list.push(project_name);
        proj_cost_list.push(cost);
        proj_year_list.push(planned_year);

    };

    console.log("Name")
    console.log(proj_name_list)
    console.log("Cost")
    console.log(proj_cost_list)
    console.log("Year")
    console.log(proj_year_list)

    var data = new FormData();

    var json_proj_name_list = JSON.stringify(project_name_list);
    var json_proj_cost_list = JSON.stringify(proj_cost_list);
    var json_proj_year_list = JSON.stringify(proj_year_list);

    console.log("JSON Name")
    console.log(json_proj_name_list)

    data.append("project_name_list",json_proj_name_list);
    data.append("project_cost_list",json_proj_cost_list);
    data.append("project_year_list",json_proj_year_list);
    data.append("facility_id", facility_id);

    var save_updates_to_db = ajax_update_database_with_file("save-updates-to-db", data); //Submitting the data through the ajax function, see main.js for the helper function.
    save_updates_to_db.done(function(return_data){ //Reset the form once the data is added successfully
    });


};

$(function() {

    // Get the Open Layers map object from the Tethys MapView
    var map = TETHYS_MAP_VIEW.getMap();

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

            document.getElementById('modal-facility-id').innerHTML = selected_feature.get('facility_id');

            var data = new FormData();
            data.append("facility_id",selected_feature.get('facility_id'));
            data.append("coordinates",selected_feature.getGeometry().getCoordinates());


            var get_project_list = ajax_update_database_with_file("get-project-list", data); //Submitting the data through the ajax function, see main.js for the helper function.
            get_project_list.done(function(return_data){

            if("project_name" in return_data){
                project_name_list = return_data.project_name;
            };

            if("cost" in return_data){
                project_cost_list = return_data.cost;
            };

            if("planned_year" in return_data){
                planned_year_list = return_data.planned_year;
            };

            $('#project-list-table tr').not(':first').remove();
            var html = '';

            for(var i = 0; i < project_name_list.length; i++){


                html += '<tr id="row-'+(i+1)+'">'+
                            '<td><input class="edit-fields project-name" type="text" id="' + (i+1) +'-project-name" value="'+ project_name_list[i] + '" disabled></td>' +
                            '<td><input class="edit-fields" type="text" id="' + (i+1) +'-project-cost" value="'+ project_cost_list[i] + '" disabled></td>' +
                            '<td><input class="edit-fields" type="text" id="' + (i+1) +'-project-year" value="'+ planned_year_list[i] + '" disabled></td>' +
                            '<td class="table-button"><div"><a name="submit-stop-edit-region" style="display:none;" id="stop-edit-button-'+(i+1)+'" onclick="stopEditRow('+(i+1)+');" class="btn btn-success submit-stop-edit-region" role="button">'+
                            '<span class="glyphicon glyphicon-save"></span> Stop Editing </a><a name="submit-edit-region" id="edit-button-'+(i+1)+'" onclick="editRow('+(i+1)+');" class="btn btn-warning submit-edit-region" role="button">'+
                            '<span class="glyphicon glyphicon-edit"></span> Edit </a><a name="submit-delete-region" id="delete-button-'+(i+1)+'" class="btn btn-danger submit-delete-region" role="button">'+
                            '<span class="glyphicon glyphicon-remove"></span> Delete </a>'+
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

    document.getElementById('stop-edit-button-'+row_num).style.display = 'table-row';
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

    document.getElementById(row_num+'-project-cost').disabled = false;
    document.getElementById(row_num+'-project-cost').style.border = '1px solid';

    document.getElementById(row_num+'-project-year').disabled = false;
    document.getElementById(row_num+'-project-year').style.border = '1px solid';

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
        edit_buttons[j].style.display = 'table-row';

    };
    document.getElementById(row_num+'-project-name').disabled = true;
    document.getElementById(row_num+'-project-name').style.border = 'none';

    document.getElementById(row_num+'-project-cost').disabled = true;
    document.getElementById(row_num+'-project-cost').style.border = 'none';

    document.getElementById(row_num+'-project-year').disabled = true;
    document.getElementById(row_num+'-project-year').style.border = 'none';

};

function addProjectRow (){

    var html = '';

        var nrows = document.querySelectorAll('.submit-delete-region');
        numrows = nrows.length;
        console.log(numrows);
        i = numrows;

        html += '<tr id="row-'+(i+1)+'">'+
                    '<td><input style="border: 1px solid" class="edit-fields" type="text" id="' + (i+1) +'-project-name" value="" ></td>' +
                    '<td><input style="border: 1px solid" class="edit-fields" type="text" id="' + (i+1) +'-project-cost" value="" ></td>' +
                    '<td><input style="border: 1px solid" class="edit-fields" type="text" id="' + (i+1) +'-project-year" value="" ></td>' +
                    '<td class="table-button"><div"><a name="submit-stop-edit-region" style="display:none;" id="stop-edit-button-'+(i+1)+'" onclick="stopEditRow('+(i+1)+');" class="btn btn-success submit-stop-edit-region" role="button">'+
                    '<span class="glyphicon glyphicon-save"></span> Stop Editing </a><a name="submit-edit-region" id="edit-button-'+(i+1)+'" onclick="editRow('+(i+1)+');" class="btn btn-warning submit-edit-region" role="button">'+
                    '<span class="glyphicon glyphicon-edit"></span> Edit </a><a name="submit-delete-region" id="delete-button-'+(i+1)+'" class="btn btn-danger submit-delete-region" role="button">'+
                    '<span class="glyphicon glyphicon-remove"></span> Delete </a>'+
                    '</div>'+
                    '</td>'+
                '</tr>';


    $('#project-list-table tr').last().after(html);
    editRow(i+1);
};