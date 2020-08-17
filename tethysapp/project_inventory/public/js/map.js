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
            //var coordinates = selected_feature.getGeometry().getCoordinates();

            document.getElementById('modal-facility-id').innerHTML = selected_feature.get('facility_id');
            document.getElementById('modal-project').value = selected_feature.get('project');
            document.getElementById('modal-cost').value = selected_feature.get('cost');
            document.getElementById('modal-planned-year').value = selected_feature.get('planned_year');

        } else {}
    });
});