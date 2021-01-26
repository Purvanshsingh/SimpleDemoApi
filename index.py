from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hydrus.app_factory import app_factory
from hydrus.utils import set_session, set_doc, set_hydrus_server_url, set_api_name
from hydra_python_core import doc_maker
from hydrus.data.db_models import Base
from creating_api_doc.api_doc_output import doc

# Define the server URL, this is what will be displayed on the Doc
HYDRUS_SERVER_URL = "http://localhost:8080/"

# The name of the API or the EntryPoint, the api will be at http://localhost/<API_NAME>
API_NAME = "movie_api"


# Define the Hydra API Documentation
# NOTE: You can use your own API Documentation and create a HydraDoc object using doc_maker
#       Or you may create your own HydraDoc Documentation using doc_writer [see hydrus/hydraspec/doc_writer_sample]
apidoc = doc_maker.create_doc(doc, HYDRUS_SERVER_URL, API_NAME)
# Define the database connection
engine = create_engine('sqlite:///database.db')
# Add the required Models to the database
Base.metadata.create_all(engine)
# Start a session with the DB and create all classes needed by the APIDoc
session = sessionmaker(bind=engine)()

# Create a hydrus app with the API name you want, default will be "api"
app = app_factory(API_NAME)

# Set the name of the API
with set_api_name(app, API_NAME):
    # Set the API Documentation
    with set_doc(app, apidoc):
        # Set HYDRUS_SERVER_URL
        with set_hydrus_server_url(app, HYDRUS_SERVER_URL):
            # Set the Database session
            with set_session(app, session):
                # Start the hydrus app
                app.run(host='127.0.0.1', debug=True, port=8080)