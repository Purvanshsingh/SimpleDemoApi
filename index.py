from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from gevent.pywsgi import WSGIServer
import logging
from hydrus.data import doc_parse
from hydrus.app_factory import app_factory
from hydrus.utils import (
    set_session, set_doc, set_hydrus_server_url,
    set_token, set_api_name, set_authentication)
from hydra_python_core import doc_maker
from hydrus.data.db_models import Base, create_database_tables
from creating_api_doc.MovieApi_doc import doc
from hydrus.socketio_factory import create_socket

logger = logging.getLogger(__file__)
# Defining server URL
HYDRUS_SERVER_URL = ""
# Defining API Name
API_NAME = "MovieApi"


apidoc = doc_maker.create_doc(doc, HYDRUS_SERVER_URL, API_NAME)
engine = create_engine('postgres://mmcsdtdaalvitt:caa15701bd57f476189b603613d7402d3c763530383f556c0d4744b186f0eaab@ec2-34-225-167-77.compute-1.amazonaws.com:5432/d4568vnmaj0f75')
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()

classes = doc_parse.get_classes(apidoc)
properties = doc_parse.get_all_properties(classes)
Base.metadata.drop_all(engine)
create_database_tables(classes)
Base.metadata.create_all(engine)
AUTH = False
TOKEN = True
app = app_factory(API_NAME)
socketio = create_socket(app, session)
#
# Nested context managers
#
# Use authentication for all requests
# Set the API Documentation
# Set HYDRUS_SERVER_URL
# Set the Database session
with set_authentication(app, AUTH), set_token(app, TOKEN), \
     set_api_name(app, API_NAME), set_doc(app, apidoc), \
     set_hydrus_server_url(app, HYDRUS_SERVER_URL), set_session(app, session):
        if __name__ == "__main__":
            # this is run only if development server is run
            # Set the name of the API
            socketio.run(app=app, debug=True, port=8080)
        else:
            # Start the Hydrus app
            http_server = WSGIServer(('', 8080), app)
            logger.info(f'Running server at port 8080')
            try:
                http_server.serve_forever()
            except KeyboardInterrupt:
                pass
