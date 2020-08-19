from tethys_gizmos.gizmo_options import PlotlyView
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

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

    df = pd.DataFrame(columns=['Construction Year', 'Estimate Cost', 'Facility ID', 'Project', 'Category'])

    for project in projects:
        df=df.append({'Construction Year': project.planned_year, 'Construction Cost': float(project.cost[0]), 'Facility ID': project.facility_id, 'Project':project.project, 'Category':project.category}, ignore_index=True)


    # Build up Plotly plot
    bargraph_px = px.bar(
        df,
        hover_data=["Facility ID", "Project"],
        x="Construction Year",
        y="Construction Cost",
        color="Category",
        title="Future Project Costs"
    )

    bargraph_px.update_layout(
        yaxis=dict(title='Construction Cost (USD)',),
        xaxis=dict(title='Construction Year'),
        legend=dict(title='Facility ID')
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

    df = pd.DataFrame(columns=['Construction Year', 'Projected Cost', 'Facility ID', 'Project'])

    for project in projects:
        df=df.append({'Construction Year': project.planned_year, 'Projected Cost': int(project.cost[0]), 'Facility ID': project.facility_id, 'Project':project.project}, ignore_index=True)


    # Build up Plotly plot
    piechart_go = go.Figure(go.Pie(
        name="",
        values=df["Projected Cost"],
        labels=df["Facility ID"],
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

    df = pd.DataFrame(columns=['Construction Year', 'Estimated Cost', 'Facility ID', 'Project', 'Category'])

    for project in projects:
        df=df.append({'Construction Year': project.planned_year, 'Estimated Cost': int(project.cost[0]), 'Facility ID': project.facility_id, 'Project':project.project, 'Category':project.category}, ignore_index=True)


    # Build up Plotly plot
    sunburst_px = px.sunburst(
        df,
        path=['Category', 'Construction Year', 'Facility ID'],
        values='Estimated Cost',
        color='Project',
    )

    sunburst_plot = PlotlyView(sunburst_px, height=height, width=width)
    session.close()
    return sunburst_plot