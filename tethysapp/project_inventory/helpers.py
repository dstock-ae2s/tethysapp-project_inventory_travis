from tethys_gizmos.gizmo_options import PlotlyView
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
from .app import ProjectInventory as app
from .model import Project, Revenue


def create_capital_costs_bargraph(height='520 px', width='100%'):
    """
    Generates a plotly view of projects
    """
    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    projects = session.query(Project).all()

    df = pd.DataFrame(columns=['Construction Year', 'Projected Cost', 'Facility ID', 'Project', 'Category'])

    for project in projects:

        if project.recur_checkbox_val == "true":
            y = 0
            for x in range(len(project.const_cost) - 1):
                df = df.append({'Construction Year': int(project.const_year) + y,
                                'Projected Cost': int(json.loads(project.const_cost[x + 1])),
                                'Facility ID': project.facility_id, 'Project': project.project,
                                'Category': project.category}, ignore_index=True)
                y = y + 1

        else:
            df = df.append(
                {'Construction Year': int(project.const_year), 'Projected Cost': int(json.loads(project.const_cost[0])),
                 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category},
                ignore_index=True)

    # Build up Plotly plot
    bargraph_px = px.bar(
        df,
        hover_data=["Facility ID", "Category", "Project", "Projected Cost"],
        x="Construction Year",
        y="Projected Cost",
        color='Category',
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

def create_capital_costs_piechart(height='520 px', width='100%'):
    """
    Generates a plotly view of projects
    """
    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    projects = session.query(Project).all()

    df = pd.DataFrame(columns=['Construction Year', 'Projected Cost', 'Facility ID', 'Project', 'Category'])

    for project in projects:


        if project.recur_checkbox_val == "true":
            y = 0
            for x in range(len(project.const_cost) - 1):
                df = df.append({'Construction Year': int(project.const_year) + y,
                                'Projected Cost': int(json.loads(project.const_cost[x + 1])),
                                'Facility ID': project.facility_id, 'Project': project.project,
                                'Category': project.category}, ignore_index=True)
                y = y + 1

        else:
            df = df.append(
                {'Construction Year': int(project.const_year), 'Projected Cost': int(json.loads(project.const_cost[0])),
                 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category},
                ignore_index=True)

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

def create_capital_costs_sunburst(height='520 px', width='100%'):
    """
    Generates a plotly view of projects
    """
    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    projects = session.query(Project).all()

    df = pd.DataFrame(columns=['Construction Year', 'Projected Cost', 'Facility ID', 'Project', 'Category'])

    for project in projects:

        if project.recur_checkbox_val == "true":
            y = 0
            for x in range(len(project.const_cost)-1):

                df = df.append({'Construction Year': int(project.const_year) + y, 'Projected Cost': int(json.loads(project.const_cost[x + 1])), 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category}, ignore_index=True)
                y = y+1

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


def create_revenue_requirements_bargraph(height='520 px', width='100%'):
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
        hover_data=["Facility ID", "Category", "Project", "Projected Cost"],
        x="Construction Year",
        y="Projected Cost",
        color='Category',
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

def create_revenue_requirements_piechart(height='520 px', width='100%'):
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

def create_revenue_requirements_sunburst(height='520 px', width='100%'):
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



def create_revenue_bargraph(height='520 px', width='100%'):
    """
    Generates a plotly view of projects
    """
    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    revenue_list = session.query(Revenue).all()


    dfhigh = pd.DataFrame(columns=['Scenario', 'Source', 'Monetary Value', 'Year'])
    dfmed = pd.DataFrame(columns=['Scenario', 'Source', 'Monetary Value', 'Year'])
    dflow = pd.DataFrame(columns=['Scenario', 'Source', 'Monetary Value', 'Year'])

    for entry in revenue_list:

        if entry.scenario == "high":

            dfhigh = dfhigh.append({'Scenario': entry.scenario, 'Source': entry.revenue_source, 'Monetary Value': int(json.loads(entry.monetary_Value)), 'Year': entry.year}, ignore_index=True)

        elif entry.scenario == "medium":
            dfmed = dfmed.append({'Scenario': entry.scenario, 'Source': entry.revenue_source,
                                    'Monetary Value': int(json.loads(entry.monetary_Value)), 'Year': entry.year},
                                   ignore_index=True)


        elif entry.scenario == "low":

            dflow = dflow.append({'Scenario': entry.scenario, 'Source': entry.revenue_source,

                                    'Monetary Value': int(json.loads(entry.monetary_Value)), 'Year': entry.year},

                                   ignore_index=True)

    # Build up Plotly plot
    bargraph_px = px.bar(
        dfmed,
        hover_data=["Source", "Monetary Value", "Year"],
        x="Year",
        y="Monetary Value",
        color="Source"
        # title="Revenue"
    )

    bargraph_px.update_layout(
        yaxis=dict(title='Revenue (USD)'),
        xaxis=dict(title='Year'),
        legend=dict(title='Source of Revenue')
    )

    bargraph_plot = PlotlyView(bargraph_px, divid="bar-plot-rev-div", height=height, width=width)
    session.close()
    return bargraph_plot

def create_revenue_piechart(height='520 px', width='100%'):
    """
    Generates a plotly view of projects
    """
    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    revenue_list = session.query(Revenue).all()

    dfhigh = pd.DataFrame(columns=['Scenario', 'Source', 'Monetary Value', 'Year'])
    dfmed = pd.DataFrame(columns=['Scenario', 'Source', 'Monetary Value', 'Year'])
    dflow = pd.DataFrame(columns=['Scenario', 'Source', 'Monetary Value', 'Year'])

    for entry in revenue_list:

        if entry.scenario == "high":

            dfhigh = dfhigh.append({'Scenario': entry.scenario, 'Source': entry.revenue_source,
                                    'Monetary Value': int(json.loads(entry.monetary_Value)), 'Year': entry.year},
                                   ignore_index=True)

        elif entry.scenario == "medium":
            dfmed = dfmed.append({'Scenario': entry.scenario, 'Source': entry.revenue_source,
                                  'Monetary Value': int(json.loads(entry.monetary_Value)), 'Year': entry.year},
                                 ignore_index=True)


        elif entry.scenario == "low":

            dflow = dflow.append({'Scenario': entry.scenario, 'Source': entry.revenue_source,

                                  'Monetary Value': int(json.loads(entry.monetary_Value)), 'Year': entry.year},

                                 ignore_index=True)
    # Build up Plotly plot
    piechart_go = go.Figure(go.Pie(
        name="",
        values=dfmed["Monetary Value"],
        labels=dfmed["Source"],
        text=dfmed["Source"],
        customdata=dfmed["Year"],
        hovertemplate="Source: %{label} <br> Scenario: %{text} <br> Year: %{customdata} <br>Revenue: %{value}"
    ))

    piechart_plot = PlotlyView(piechart_go, divid="pie-plot-rev-div", height=height, width=width)
    session.close()
    return piechart_plot

def create_revenue_sunburst(height='520 px', width='100%'):
    """
    Generates a plotly view of projects
    """
    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    revenue_list = session.query(Revenue).all()

    dfhigh = pd.DataFrame(columns=['Scenario', 'Source', 'Monetary Value', 'Year'])
    dfmed = pd.DataFrame(columns=['Scenario', 'Source', 'Monetary Value', 'Year'])
    dflow = pd.DataFrame(columns=['Scenario', 'Source', 'Monetary Value', 'Year'])

    for entry in revenue_list:

        if entry.scenario == "high":

            dfhigh = dfhigh.append({'Scenario': entry.scenario, 'Source': entry.revenue_source,
                                    'Monetary Value': int(json.loads(entry.monetary_Value)), 'Year': entry.year},
                                   ignore_index=True)

        elif entry.scenario == "medium":
            dfmed = dfmed.append({'Scenario': entry.scenario, 'Source': entry.revenue_source,
                                  'Monetary Value': int(json.loads(entry.monetary_Value)), 'Year': entry.year},
                                 ignore_index=True)


        elif entry.scenario == "low":

            dflow = dflow.append({'Scenario': entry.scenario, 'Source': entry.revenue_source,
                                  'Monetary Value': int(json.loads(entry.monetary_Value)), 'Year': entry.year},
                                 ignore_index=True)
    # Build up Plotly plot
    sunburst_px = px.sunburst(
        dfmed,
        path=['Source', 'Year','Monetary Value'],
        values='Monetary Value',
        color='Source',
        labels=dfmed["Source"],
        # text=df["Project"],
        # customdata=df["Construction Year"],
        # hovertemplate="Facility ID: %{label} <br>Project: %{path[2]} <br>Construction Year: %{customdata} <br>Cost: %{value}"

    )

    sunburst_plot = PlotlyView(sunburst_px, divid="sun-plot-rev-div",height=height, width=width)
    session.close()
    return sunburst_plot


def create_revenue_vs_requirements_bargraph(height='520 px', width='100%'):
    """
    Generates a plotly view of projects
    """
    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    projects = session.query(Project).all()

    dfrevreq = pd.DataFrame(columns=['Construction Year', 'Projected Cost', 'Facility ID', 'Project', 'Category'])

    for project in projects:

        if project.debt_checkbox_val == "true":
            z =1
            for c in range(len(project.const_cost)-1):
                dfrevreq = dfrevreq.append({'Construction Year': int(project.const_year) + z, 'Projected Cost': int(json.loads(project.const_cost[c + 1])), 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category}, ignore_index=True)
                z = z+1
        elif project.recur_checkbox_val == "true":
            y = 0
            for x in range(len(project.const_cost)-1):

                dfrevreq = dfrevreq.append({'Construction Year': int(project.const_year) + y, 'Projected Cost': int(json.loads(project.const_cost[x + 1])), 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category}, ignore_index=True)
                y = y+1
        else:
            dfrevreq = dfrevreq.append({'Construction Year': int(project.const_year), 'Projected Cost': int(json.loads(project.const_cost[0])), 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category}, ignore_index=True)

    # Build up Plotly plot
    bargraph_px = px.bar(
        dfrevreq,
        hover_data=["Facility ID", "Category", "Project", "Projected Cost"],
        x="Construction Year",
        y="Projected Cost",
        color='Category',
        # title="Future Project Costs"
    )

    bargraph_px.update_layout(
        yaxis=dict(title='Construction Cost (USD)',),
        xaxis=dict(title='Construction Year'),
        legend=dict(title='Category')
    )
    bargraph_px.add_scatter(y=[10000, 20000, 35000], x=[2020,2021,2022], mode="lines",
                    line=dict(width=4,color="Red"),
                    name="scattertest")



    bargraph_plot = PlotlyView(bargraph_px, height=height, width=width)
    session.close()
    return bargraph_plot

def create_revenue_vs_requirements_piechart(height='520 px', width='100%'):
    """
    Generates a plotly view of projects
    """
    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    projects = session.query(Project).all()

    dfrevreq = pd.DataFrame(columns=['Construction Year', 'Projected Cost', 'Facility ID', 'Project', 'Category'])

    for project in projects:

        if project.debt_checkbox_val == "true":
            z = 1
            for c in range(len(project.const_cost) - 1):
                dfrevreq = dfrevreq.append({'Construction Year': int(project.const_year) + z,
                                            'Projected Cost': int(json.loads(project.const_cost[c + 1])),
                                            'Facility ID': project.facility_id, 'Project': project.project,
                                            'Category': project.category}, ignore_index=True)
                z = z + 1
        elif project.recur_checkbox_val == "true":
            y = 0
            for x in range(len(project.const_cost) - 1):
                dfrevreq = dfrevreq.append({'Construction Year': int(project.const_year) + y,
                                            'Projected Cost': int(json.loads(project.const_cost[x + 1])),
                                            'Facility ID': project.facility_id, 'Project': project.project,
                                            'Category': project.category}, ignore_index=True)
                y = y + 1
        else:
            dfrevreq = dfrevreq.append(
                {'Construction Year': int(project.const_year), 'Projected Cost': int(json.loads(project.const_cost[0])),
                 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category},
                ignore_index=True)

    # Build up Plotly plot
    piechart_go = go.Figure(go.Pie(
        name="",
        values=dfrevreq["Projected Cost"],
        labels=dfrevreq["Category"],
        text=dfrevreq["Project"],
        customdata=dfrevreq["Construction Year"],
        hovertemplate="Facility ID: %{label} <br>Project: %{text} <br>Construction Year: %{customdata} <br>Cost: %{value}"
    ))

    piechart_plot = PlotlyView(piechart_go, height=height, width=width)
    session.close()
    return piechart_plot

def create_revenue_vs_requirements_sunburst(height='520 px', width='100%'):
    """
    Generates a plotly view of projects
    """
    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    projects = session.query(Project).all()

    dfrevreq = pd.DataFrame(columns=['Construction Year', 'Projected Cost', 'Facility ID', 'Project', 'Category'])

    for project in projects:

        if project.debt_checkbox_val == "true":
            z = 1
            for c in range(len(project.const_cost) - 1):
                dfrevreq = dfrevreq.append({'Construction Year': int(project.const_year) + z,
                                            'Projected Cost': int(json.loads(project.const_cost[c + 1])),
                                            'Facility ID': project.facility_id, 'Project': project.project,
                                            'Category': project.category}, ignore_index=True)
                z = z + 1
        elif project.recur_checkbox_val == "true":
            y = 0
            for x in range(len(project.const_cost) - 1):
                dfrevreq = dfrevreq.append({'Construction Year': int(project.const_year) + y,
                                            'Projected Cost': int(json.loads(project.const_cost[x + 1])),
                                            'Facility ID': project.facility_id, 'Project': project.project,
                                            'Category': project.category}, ignore_index=True)
                y = y + 1
        else:
            dfrevreq = dfrevreq.append(
                {'Construction Year': int(project.const_year), 'Projected Cost': int(json.loads(project.const_cost[0])),
                 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category},
                ignore_index=True)



    # Build up Plotly plot
    sunburst_px = px.sunburst(
        dfrevreq,
        path=['Category', 'Facility ID','Project'],
        values='Projected Cost',
        color='Category',
        labels=dfrevreq["Category"],
        # text=df["Project"],
        # customdata=df["Construction Year"],
        # hovertemplate="Facility ID: %{label} <br>Project: %{path[2]} <br>Construction Year: %{customdata} <br>Cost: %{value}"

    )

    sunburst_plot = PlotlyView(sunburst_px, height=height, width=width)
    session.close()
    return sunburst_plot