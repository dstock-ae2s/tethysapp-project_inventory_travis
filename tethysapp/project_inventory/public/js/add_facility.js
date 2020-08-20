$(function(){
    $('#add_project_estcost').change(function(){updateConstCost();});
    $('#add_project_estyear').change(function(){updateConstCost();});
    $('#add_project_constyear').change(function(){updateConstCost();});
});

function updateConstCost(){
    this_est_cost = parseFloat(document.getElementById('add_project_estcost').value)
    this_const_year = parseFloat(document.getElementById('add_project_constyear').value)
    this_est_year = parseFloat(document.getElementById('add_project_estyear').value)
    document.getElementById('add_project_constcost').value = ((this_est_cost*Math.pow(1.04,(this_const_year-this_est_year))).toFixed(0)).toString();
};