function importProjectsToDb(){
    var data = new FormData();
    var import_projects_to_db = ajax_update_database_with_file("import-projects-to-db", data); //Submitting the data through the ajax function, see main.js for the helper function.
    import_projects_to_db.done(function(return_data){
        if ('success' in return_data) {
            alert("import successful")//Reset the form once the data is added successfully
        }//Reset the form once the data is added successfully
    });

}

function importRevenueToDb(){
    var data = new FormData();
    var import_revenue_to_db = ajax_update_database_with_file("import-revenue-to-db", data); //Submitting the data through the ajax function, see main.js for the helper function.
    import_revenue_to_db.done(function(return_data){
        if ('success' in return_data) {
            alert("import successful")//Reset the form once the data is added successfully
        }
    });

}

function eraseProjectsFromDb(){
    var data = new FormData();
    var erase_projects_from_db = ajax_update_database_with_file("erase-projects-from-db", data); //Submitting the data through the ajax function, see main.js for the helper function.
    erase_projects_from_db.done(function(return_data){
        if ('success' in return_data) {
            alert("All projects have been deleted")//Reset the form once the data is added successfully
        }//Reset the form once the data is added successfully
    });

}

function eraseRevenueFromDb(){
    var data = new FormData();
    var erase_revenue_from_db = ajax_update_database_with_file("erase-revenue-from-db", data); //Submitting the data through the ajax function, see main.js for the helper function.
    erase_revenue_from_db.done(function(return_data){
         if ('success' in return_data) {
            alert("All revenue data has been deleted")//Reset the form once the data is added successfully
         }//Reset the form once the data is added successfully
    });

}
