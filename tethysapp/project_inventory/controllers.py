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
import numpy as np


@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    # Get list of projects and create projects MVLayer:
    projects = get_all_projects()
    ww_features = []
    w_features = []
    sw_features = []
    fac_features = []
    golf_features = []
    transp_features = []
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
                'planned_year': project.planned_year,
                'category': project.category,
                'description': project.description,
                'priority': project.priority,
                'est_year': project.est_year,
                'const_cost': project.const_cost
            }
        }

        if project.category == "Wastewater":
            ww_features.append(project_feature)
        elif project.category == "Stormwater":
            sw_features.append(project_feature)
        elif project.category == "Facilities":
            fac_features.append(project_feature)
        elif project.category == "Golf":
            fac_features.append(project_feature)
        elif project.category == "Transportation":
            fac_features.append(project_feature)
        else:
            w_features.append(project_feature)

    # Define GeoJSON FeatureCollections
    sw_projects_feature_collection = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'EPSG:4326'
            }
        },
        'features': sw_features
    }
    w_projects_feature_collection = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'EPSG:4326'
            }
        },
        'features': w_features
    }
    ww_projects_feature_collection = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'EPSG:4326'
            }
        },
        'features': ww_features
    }
    fac_projects_feature_collection = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'EPSG:4326'
            }
        },
        'features': fac_features
    }
    golf_projects_feature_collection = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'EPSG:4326'
            }
        },
        'features': golf_features
    }
    transp_projects_feature_collection = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'EPSG:4326'
            }
        },
        'features': transp_features
    }

    sw_style = {'ol.style.Style': {
        'image': {'ol.style.RegularShape': {
            'radius': 10,
            'points': 4,
            'angle': np.pi / 4,
            'fill': {'ol.style.Fill': {
                'color':  '#03fc45'
            }},
            'stroke': {'ol.style.Stroke': {
                'color': '#ffffff',
                'width': 1
            }}
        }}
    }}

    w_style = {'ol.style.Style': {
        'image': {'ol.style.Circle': {
            'radius': 10,
            'fill': {'ol.style.Fill': {
                'color': '#d84e1f'
            }},
            'stroke': {'ol.style.Stroke': {
                'color': '#ffffff',
                'width': 1
            }}
        }}
    }}

    ww_style = {'ol.style.Style': {
        'image': {'ol.style.RegularShape': {
            'radius': 10,
            'points': 3,
            'rotation': np.pi / 4,
            'angle': 0,
            'fill': {'ol.style.Fill': {
                'color': '#fc0303'
            }},
            'stroke': {'ol.style.Stroke': {
                'color': '#ffffff',
                'width': 1
            }}
        }}
    }}

    fac_style = {'ol.style.Style': {
        'image': {'ol.style.Circle': {
            'radius': 10,
            'fill': {'ol.style.Fill': {
                'color': '#fcba03'
            }},
            'stroke': {'ol.style.Stroke': {
                'color': '#ffffff',
                'width': 1
            }}
        }}
    }}

    golf_style = {'ol.style.Style': {
        'image': {'ol.style.Circle': {
            'radius': 10,
            'fill': {'ol.style.Fill': {
                'color': '#a6a49f'
            }},
            'stroke': {'ol.style.Stroke': {
                'color': '#ffffff',
                'width': 1
            }}
        }}
    }}

    transp_style = {'ol.style.Style': {
        'image': {'ol.style.Circle': {
            'radius': 10,
            'fill': {'ol.style.Fill': {
                'color': '#c000fa'
            }},
            'stroke': {'ol.style.Stroke': {
                'color': '#ffffff',
                'width': 1
            }}
        }}
    }}

    # Create a Map View Layer
    sw_projects_layer = MVLayer(
        source='GeoJSON',
        options=sw_projects_feature_collection,
        legend_title='projects',
        layer_options={'style': sw_style},
        feature_selection=True
    )
    w_projects_layer = MVLayer(
        source='GeoJSON',
        options=w_projects_feature_collection,
        legend_title='projects',
        layer_options={'style': w_style},
        feature_selection=True
    )
    ww_projects_layer = MVLayer(
        source='GeoJSON',
        options=ww_projects_feature_collection,
        legend_title='projects',
        layer_options={'style': ww_style},
        feature_selection=True
    )
    fac_projects_layer = MVLayer(
        source='GeoJSON',
        options=fac_projects_feature_collection,
        legend_title='projects',
        layer_options={'style': fac_style},
        feature_selection=True
    )
    golf_projects_layer = MVLayer(
        source='GeoJSON',
        options=golf_projects_feature_collection,
        legend_title='projects',
        layer_options={'style': golf_style},
        feature_selection=True
    )
    transp_projects_layer = MVLayer(
        source='GeoJSON',
        options=transp_projects_feature_collection,
        legend_title='projects',
        layer_options={'style': transp_style},
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
        layers=[sw_projects_layer, w_projects_layer, ww_projects_layer,
                fac_projects_layer, golf_projects_layer, transp_projects_layer],
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
        display_text='Add Facility',
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
    category = ''
    description = ''
    priority = ''
    est_year = ''
    const_cost = ''


    # Errors
    facility_id_error = ''
    project_error = ''
    cost_error = ''
    date_error = ''
    location_error = ''
    category_error = ''
    description_error = ''
    priority_error = ''
    est_year_error = ''
    const_cost_error = ''

    # Handle form submission
    if request.POST and 'add-button' in request.POST:
        # Get values
        has_errors = False
        facility_id = request.POST.get('facility_id', None)
        project = request.POST.get('project', None)
        cost = request.POST.get('cost', None)
        planned_year = request.POST.get('planned_year', None)
        location = request.POST.get('geometry', None)
        category = request.POST.get('category', None)
        description = request.POST.get('description', None)
        priority = request.POST.get('priority', None)
        est_year = request.POST.get('est_year', None)
        const_cost = request.POST.get('const_cost', None)
        checked = request.POST.get('add_project_checkbox')


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

        if not category:
            has_errors = True
            category_error = 'Category is required.'

        if not description:
            has_errors = True
            description_error = 'Description is required.'

        if not priority:
            has_errors = True
            priority_error = 'Priority is required.'

        if not est_year:
            has_errors = True
            est_year_error = 'Estimate Year is required.'

        if not const_cost:
            has_errors = True
            const_cost_error = 'Construction Cost is required.'

        if not has_errors:
            # Get value of max_projects custom setting
            max_projects = app.get_custom_setting('max_projects')

            # Query database for count of projects
            Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
            session = Session()
            num_projects = session.query(Project).count()

            # Only add the project if custom setting doesn't exist or we have not exceed max_projects
            if not max_projects or num_projects < max_projects:
                add_new_project(location=location, facility_id=facility_id, project=project, cost=cost, planned_year=planned_year, category=category, description=description, priority=priority, est_year=est_year, const_cost=const_cost, checkbox=checked)
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
        display_text='Estimated Cost',
        name='cost',
        initial=cost,
        error=cost_error
    )

    description_input = TextInput(
        display_text='Description',
        name='description',
        initial=description,
        error=description_error
    )

    const_cost_input = TextInput(
        display_text='Construction Cost',
        name='const_cost',
        initial=const_cost,
        error=const_cost_error
    )

    est_year_input = TextInput(
        display_text='Estimate Year',
        name='est_year',
        initial=est_year,
        error=est_year_error
    )

    planned_year_input = DatePicker(
        name='planned_year',
        display_text='Construction Year',
        autoclose=True,
        format='yyyy',
        start_view='decade',
        today_button=True,
        initial=planned_year,
        error=date_error
    )

    category_input = SelectInput(
        display_text='Category',
        name='category',
        multiple=False,
        options=[('Water', 'Water'), ('Wastewater', 'Wastewater'), ('Stormwater', 'Stormwater'),
                 ('Facilities', 'Facilities'), ('Golf', 'Golf'), ('Transportation', 'Transportation')],
        initial=['Water'],
        error=category_error
    )

    priority_input = SelectInput(
        display_text='Priority',
        name='priority',
        multiple=False,
        options=[('One', '1'), ('Two', '2'), ('Three', '3'), ('Four', '4')],
        initial=['One'],
        error=priority_error
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
        'est_year_input': est_year_input,
        'category_input': category_input,
        'description_input': description_input,
        'priority_input': priority_input,
        'const_cost_input': const_cost_input,
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
                project.facility_id, project.category,
                project.project, project.description, project.priority,
                project.est_year, project.cost[0],
                project.planned_year, project.const_cost,
            )
        )

    projects_table = DataTableView(
        column_names=('Facility ID', 'Category', 'Project', 'Description', 'Priority', 'Estimate Year', 'Estimated Cost', 'Construction Year', 'Construction Cost'),
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