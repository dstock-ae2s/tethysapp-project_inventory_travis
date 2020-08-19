from django.utils.html import format_html
from django.contrib import messages
from django.shortcuts import render, reverse, redirect
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import (Button, MapView, TextInput, DatePicker, 
                               SelectInput, DataTableView, MVDraw, MVView,
                               MVLayer)
from tethys_sdk.permissions import permission_required, has_permission
from .model import Project, add_new_project, get_all_projects
from .app import ProjectInventory as app
from .helpers import create_bargraph, create_piechart


@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    # Get list of projects and create projects MVLayer:
    projects = get_all_projects()
    features = []
    lat_list = []
    lng_list = []

    for project in projects:
        lat_list.append(project.latitude)
        lng_list.append(project.longitude)

        project_feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [project.longitude, project.latitude],

            },
            'properties': {
                'id': project.id,
                'facility_id': project.facility_id,
                'project': project.project,
                'cost': project.cost,
                'planned_year': project.planned_year
            }
        }
        features.append(project_feature)

    # Define GeoJSON FeatureCollection
    projects_feature_collection = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'EPSG:4326'
            }
        },
        'features': features
    }

    style = {'ol.style.Style': {
        'image': {'ol.style.Circle': {
            'radius': 10,
            'fill': {'ol.style.Fill': {
                'color':  '#d84e1f'
            }},
            'stroke': {'ol.style.Stroke': {
                'color': '#ffffff',
                'width': 1
            }}
        }}
    }}

    # Create a Map View Layer
    projects_layer = MVLayer(
        source='GeoJSON',
        options=projects_feature_collection,
        legend_title='projects',
        layer_options={'style': style},
        feature_selection=True
    )

    # Define view centered on project locations
    try:
        view_center = [sum(lng_list) / float(len(lng_list)), sum(lat_list) / float(len(lat_list))]
    except ZeroDivisionError:
        view_center = [-98.6, 39.8]

    view_options = MVView(
        projection='EPSG:4326',
        center=view_center,
        zoom=4.5,
        maxZoom=18,
        minZoom=2
    )

    project_inventory_map = MapView(
        height='100%',
        width='100%',
        layers=[projects_layer],
        basemap=[
            'CartoDB',
            {'CartoDB': {'style': 'dark'}},
            'OpenStreetMap',
            'Stamen',
            'ESRI'
        ],
        view=view_options
    )

    add_project_button = Button(
        display_text='Add project',
        name='add-project-button',
        icon='glyphicon glyphicon-plus',
        style='success',
        href=reverse('project_inventory:add_project')
    )

    context = {
        'project_inventory_map': project_inventory_map,
        'add_project_button': add_project_button,
        'can_add_projects': has_permission(request, 'add_projects')
    }

    return render(request, 'project_inventory/home.html', context)


@permission_required('add_projects')
def add_project(request):
    """
    Controller for the Add project page.
    """
    # Default Values
    facility_id = ''
    project = ''
    cost = ''
    planned_year = ''
    location = ''

    # Errors
    facility_id_error = ''
    project_error = ''
    cost_error = ''
    date_error = ''
    location_error = ''

    # Handle form submission
    if request.POST and 'add-button' in request.POST:
        # Get values
        has_errors = False
        facility_id = request.POST.get('facility_id', None)
        project = request.POST.get('project', None)
        cost = request.POST.get('cost', None)
        planned_year = request.POST.get('planned_year', None)
        location = request.POST.get('geometry', None)

        # Validate
        if not facility_id:
            has_errors = True
            facility_id_error = 'Facility ID is required.'

        if not project:
            has_errors = True
            project_error = 'Project Name is required.'

        if not cost:
            has_errors = True
            cost_error = 'Cost is required.'

        if not planned_year:
            has_errors = True
            date_error = 'Planned Year is required.'

        if not location:
            has_errors = True
            location_error = 'Location is required.'

        if not has_errors:
            # Get value of max_projects custom setting
            max_projects = app.get_custom_setting('max_projects')

            # Query database for count of projects
            Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
            session = Session()
            num_projects = session.query(Project).count()

            # Only add the project if custom setting doesn't exist or we have not exceed max_projects
            if not max_projects or num_projects < max_projects:
                add_new_project(location=location, facility_id=facility_id, project=project, cost=cost, planned_year=planned_year)
            else:
                messages.warning(request, 'Unable to add project "{0}", because the inventory is full.'.format(facility_id))

            return redirect(reverse('project_inventory:home'))

        messages.error(request, "Please fix errors.")

    # Define form gizmos
    facility_id_input = TextInput(
        display_text='Facility ID',
        name='facility_id',
        initial=facility_id,
        error=facility_id_error
    )

    project_input = TextInput(
        display_text='Project Name',
        name='project',
        initial=project,
        error=project_error
    )

    cost_input = TextInput(
        display_text='Cost',
        name='cost',
        initial=cost,
        error=cost_error
    )

    planned_year_input = DatePicker(
        name='planned_year',
        display_text='Planned Year',
        autoclose=True,
        format='yyyy',
        start_view='decade',
        today_button=True,
        initial=planned_year,
        error=date_error
    )

    initial_view = MVView(
        projection='EPSG:4326',
        center=[-98.6, 39.8],
        zoom=3.5
    )

    drawing_options = MVDraw(
        controls=['Modify', 'Delete', 'Move', 'Point'],
        initial='Point',
        output_format='GeoJSON',
        point_color='#FF0000'
    )

    location_input = MapView(
        height='300px',
        width='100%',
        basemap=[
            'CartoDB',
            {'CartoDB': {'style': 'dark'}},
            'OpenStreetMap',
            'Stamen',
            'ESRI'
        ],
        draw=drawing_options,
        view=initial_view
    )

    add_button = Button(
        display_text='Add',
        name='add-button',
        icon='glyphicon glyphicon-plus',
        style='success',
        attributes={'form': 'add-project-form'},
        submit=True
    )

    cancel_button = Button(
        display_text='Cancel',
        name='cancel-button',
        href=reverse('project_inventory:home')
    )

    context = {
        'facility_id_input': facility_id_input,
        'project_input': project_input,
        'cost_input': cost_input,
        'planned_year_input': planned_year_input,
        'location_input': location_input,
        'location_error': location_error,
        'add_button': add_button,
        'cancel_button': cancel_button,
        'can_add_projects': has_permission(request, 'add_projects')
    }

    return render(request, 'project_inventory/add_project.html', context)


@login_required()
def list_projects(request):
    """
    Show all projects in a table view.
    """
    projects = get_all_projects()
    table_rows = []

    for project in projects:

        table_rows.append(
            (
                project.facility_id, project.project,
                project.cost, project.planned_year
            )
        )

    projects_table = DataTableView(
        column_names=('Facility ID', 'Project', 'Cost', 'Planned Year'),
        rows=table_rows,
        searching=True,
        orderClasses=False,
        lengthMenu=[[10, 25, 50, -1], [10, 25, 50, "All"]],
    )

    context = {
        'projects_table': projects_table,
        'can_add_projects': has_permission(request, 'add_projects')
    }

    return render(request, 'project_inventory/list_projects.html', context)

@login_required()
def graphs(request):
    """
    Controller for the Plots Page.
    """
    # Get projects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()

    bargraph_plot = create_bargraph()
    piechart_plot = create_piechart()

    context = {
        'bargraph_plot': bargraph_plot,
        'piechart_plot': piechart_plot,
        'can_add_projects': has_permission(request, 'add_projects')
    }

    session.close()
    return render(request, 'project_inventory/graphs.html', context)