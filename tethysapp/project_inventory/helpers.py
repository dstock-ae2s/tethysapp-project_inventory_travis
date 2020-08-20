from tethys_gizmos.gizmo_options import PlotlyView
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json


from .app import ProjectInventory as app
from .model import Project

def create_bargraph(height='520 px', width='100%'):
    """
    Generates a plotly view of projects
    """
    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    projects = session.query(Project).all()

    df = pd.DataFrame(columns=['Construction Year', 'Projected Cost', 'Facility ID', 'Project', 'Category'])

    for project in projects:
        print(project.debt_checkbox_val)
        print(project.recur_checkbox_val)
        if project.debt_checkbox_val == "true":
            z =1
            for c in range(len(project.const_cost)-1):
                df = df.append({'Construction Year': int(project.const_year) + z, 'Projected Cost': int(json.loads(project.const_cost[c + 1])), 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category}, ignore_index=True)
                z = z+1
        elif project.recur_checkbox_val == "true":
            y = 0
            for x in range(len(project.const_cost)-1):

                df = df.append({'Construction Year': int(project.const_year) + y, 'Projected Cost': int(json.loads(project.const_cost[x + 1])), 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category}, ignore_index=True)
                y = y+1
        else:
            df = df.append({'Construction Year': int(project.const_year), 'Projected Cost': int(json.loads(project.const_cost[0])), 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category}, ignore_index=True)


    # Build up Plotly plot
    bargraph_px = px.bar(
        df,
        hover_data=["Facility ID", "Project", "Projected Cost"],
        x="Construction Year",
        y="Projected Cost",
        color="Category",
        # title="Future Project Costs"
    )

    bargraph_px.update_layout(
        yaxis=dict(title='Construction Cost (USD)',),
        xaxis=dict(title='Construction Year'),
        legend=dict(title='Category')
    )

    bargraph_plot = PlotlyView(bargraph_px, height=height, width=width)
    session.close()
    return bargraph_plot

def create_piechart(height='520 px', width='100%'):
    """
    Generates a plotly view of projects
    """
    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    projects = session.query(Project).all()

    df = pd.DataFrame(columns=['Construction Year', 'Projected Cost', 'Facility ID', 'Project', 'Category'])

    for project in projects:
        if project.debt_checkbox_val == "true":
            z = 1
            for c in range(len(project.const_cost)-1):
                df = df.append({'Construction Year': int(project.const_year) + z, 'Projected Cost': int(json.loads(project.const_cost[c + 1])),
                                'Facility ID': project.facility_id, 'Project': project.project,
                                'Category': project.category}, ignore_index=True)
                z = z+1
        elif project.recur_checkbox_val == "true":
            y = 0
            for x in range(len(project.const_cost)-1):
                df = df.append({'Construction Year': int(project.const_year) + y, 'Projected Cost': int(json.loads(project.const_cost[x + 1])),
                                'Facility ID': project.facility_id, 'Project': project.project,
                                'Category': project.category}, ignore_index=True)
                y = y+1
        else:
            df = df.append({'Construction Year': int(project.const_year), 'Projected Cost': int(json.loads(project.const_cost[0])),
                            'Facility ID': project.facility_id, 'Project': project.project,
                            'Category': project.category}, ignore_index=True)

    # Build up Plotly plot
    piechart_go = go.Figure(go.Pie(
        name="",
        values=df["Projected Cost"],
        labels=df["Category"],
        text=df["Project"],
        customdata=df["Construction Year"],
        hovertemplate="Facility ID: %{label} <br>Project: %{text} <br>Construction Year: %{customdata} <br>Cost: %{value}"
    ))

    piechart_plot = PlotlyView(piechart_go, height=height, width=width)
    session.close()
    return piechart_plot

def create_sunburst(height='520 px', width='100%'):
    """
    Generates a plotly view of projects
    """
    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    projects = session.query(Project).all()

    df = pd.DataFrame(columns=['Construction Year', 'Projected Cost', 'Facility ID', 'Project', 'Category'])

    for project in projects:
        if project.debt_checkbox_val == "true":
            z = 1
            for c in range(len(project.const_cost)-1):
                df=df.append({'Construction Year': int(project.const_year) + z, 'Projected Cost': int(json.loads(project.const_cost[c + 1])), 'Facility ID': project.facility_id, 'Project':project.project, 'Category':project.category}, ignore_index=True)
                z=z+1
        elif project.recur_checkbox_val == "true":
            y=0
            for x in range(len(project.const_cost)-1):
                df = df.append({'Construction Year': int(project.const_year) + y, 'Projected Cost': int(json.loads(project.const_cost[x + 1])), 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category}, ignore_index=True)
                y=y+1
        else:
            df = df.append({'Construction Year': int(project.const_year), 'Projected Cost': int(json.loads(project.const_cost[0])), 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category}, ignore_index=True)

    # Build up Plotly plot
    sunburst_px = px.sunburst(
        df,
        path=['Category', 'Facility ID','Project'],
        values='Projected Cost',
        color='Category',
        labels=df["Category"],
        # text=df["Project"],
        # customdata=df["Construction Year"],
        # hovertemplate="Facility ID: %{label} <br>Project: %{path[2]} <br>Construction Year: %{customdata} <br>Cost: %{value}"

    )

    sunburst_plot = PlotlyView(sunburst_px, height=height, width=width)
    session.close()
    return sunburst_plot