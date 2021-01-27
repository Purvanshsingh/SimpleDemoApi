from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hydrus.app_factory import app_factory
from hydrus.utils import set_session, set_doc, set_hydrus_server_url, set_api_name
from hydra_python_core import doc_maker
from hydrus.data.db_models import Base
from creating_api_doc.api_doc_output import doc

# Server URL
HYDRUS_SERVER_URL = "http://localhost:8080/"

# Name of the API
API_NAME = "MovieApi"

# Defining the Hydra API Documentation
apidoc = doc_maker.create_doc(doc, HYDRUS_SERVER_URL, API_NAME)
# Connecting to Database
engine = create_engine('sqlite:///database.db')
# Adding required Models to the database
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()

# Creating hydrus app"
app = app_factory(API_NAME)

with set_api_name(app, API_NAME):
    # Set the API Documentation
    with set_doc(app, apidoc):
        # Set HYDRUS_SERVER_URL
        with set_hydrus_server_url(app, HYDRUS_SERVER_URL):
            # Set the Database session
            with set_session(app, session):
                # Start the hydrus app
                app.run(host='127.0.0.1', debug=True, port=8080)