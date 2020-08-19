import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, ForeignKey, ARRAY
from sqlalchemy.orm import sessionmaker, relationship

from .app import ProjectInventory as app

Base = declarative_base()


# SQLAlchemy ORM definition for the projects table
class Revenue(Base):
    """
    SQLAlchemy Project DB Model
    """
    __tablename__ = 'revenue'

    # Columns
    id = Column(Integer, primary_key=True)
    revenue_source = Column(String)
    monetary_Value = Column(String)
    year = Column(String)

class Project(Base):
    """
    SQLAlchemy Project DB Model
    """
    __tablename__ = 'projects'

    # Columns
    id = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    facility_id = Column(String)
    project = Column(String)
    cost = Column(ARRAY(String))
    planned_year = Column(String)
    category = Column(String)
    description = Column(String)
    priority = Column(String)
    est_year = Column(String)
    const_cost = Column(String)


def add_new_project(location, facility_id, project, cost, planned_year, category, description, priority, est_year, const_cost, checkbox):
    """
    Persist new project.
    """
    # Convert GeoJSON to Python dictionary
    location_dict = json.loads(location)
    location_geometry = location_dict['geometries'][0]
    longitude = location_geometry['coordinates'][0]
    latitude = location_geometry['coordinates'][1]

    interest_rate = 0.04
    pay_period = 20

    cost_array = []
    cost_array.append(cost)
    if checkbox=="true":
        annual_payment = float(cost) * (
                (interest_rate * (1 + interest_rate) ** (pay_period)) / (
                (1 + interest_rate) ** (pay_period) - 1))
        for _ in range(pay_period-1):
            cost_array.append(annual_payment)

    # Create new Project record
    new_project = Project(
        latitude=latitude,
        longitude=longitude,
        facility_id=facility_id,
        project=project,
        cost=cost_array,
        planned_year=planned_year,
        category=category,
        description=description,
        priority=priority,
        est_year=est_year,
        const_cost=const_cost
    )

    # Get connection/session to database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()

    # Add the new project record to the session
    session.add(new_project)

    # Commit the session and close the connection
    session.commit()
    session.close()


def get_all_projects():
    """
    Get all persisted projects.
    """
    # Get connection/session to database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()

    # Query for all project records
    projects = session.query(Project).all()
    session.close()

    return projects

def init_primary_db(engine, first_time):
    """
    Initializer for the primary database.
    """
    # Create all the tables
    Base.metadata.create_all(engine)

    # Add data
    if first_time:
        # Make session
        Session = sessionmaker(bind=engine)
        session = Session()

        # Initialize database with two projects
        project1 = Project(
            latitude=40.406624,
            longitude=-111.529133,
            facility_id="Deer Creek",
            project="New Intake",
            cost=["1000"],
            planned_year="2020",
            category="Water",
            description="Replace Deer Creek intake structure",
            priority="4",
            est_year="1993",
            const_cost="2000"
        )

        project2 = Project(
            latitude=40.598168,
            longitude=-111.424055,
            facility_id="Jordanelle",
            project="Clean Water",
            cost=["2000"],
            planned_year="2020",
            category="Stormwater",
            description="Clean up Jordanelle",
            priority="4",
            est_year="1941",
            const_cost="5000"
        )

        # Add the projects to the session, commit, and close
        session.add(project1)
        session.add(project2)
        session.commit()
        session.close()