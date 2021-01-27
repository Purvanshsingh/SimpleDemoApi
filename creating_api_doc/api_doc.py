from hydra_python_core.doc_writer import HydraDoc
from hydra_python_core.doc_writer import HydraClass
from hydra_python_core.doc_writer import HydraClassProp
from hydra_python_core.doc_writer import HydraClassOp, HydraStatus
from hydra_python_core.doc_writer import HydraCollection

API_NAME = "movie_api"
BASE_URL = "http://localhost:8080/"

# Creating ApiDoc
api_doc = api_doc = HydraDoc(API_NAME,
                             "The Description for the movie API",
                             "This API lets you see the list of good movies and gives you the ability to modify the "
                             "list",
                             API_NAME,
                             BASE_URL,
                             "vocab")

# Creating Movie class for Api
class_title = "Movie"
class_description = "The class of the Movie"
movie_class_ = HydraClass(class_title, class_description)

# Defining properties for the Movie class

prop1_uri = "http://localhost:8080/props_movie_name"
prop1_title = "movie_name"
movie_name_prop = HydraClassProp(prop1_uri, prop1_title,
                                 required=True, read=True, write=True)

prop2_uri = "http://localhost:8080/props_movie_director"
prop2_title = "movie_director"
movie_director_prop = HydraClassProp(prop2_uri, prop1_title,
                                     required=True, read=True, write=True)

# Creating operations fort the class

update_operation = "UpdateMovie"
update_operation_method = "POST"
update_operation_expects = movie_class_.id_
update_operation_returns = None
update_operation_returns_header = ["Content-Type", "Content-Length"]
update_operation_expects_header = []
# List of statusCode for the operation
update_operation_status = [HydraStatus(code=200, desc="Movie class updated.")]

add_operation = "AddMovie"
add_operation_method = "PUT"
add_operation_expects = movie_class_.id_
add_operation_returns = None  # URI of the object that is returned by the operation
add_operation_returns_header = ["Content-Type", "Content-Length"]
add_operation_expects_header = []
# List of statusCode for the operation
add_operation_status = [HydraStatus(code=200, desc="Movie class Added.")]

get_operation = "GetMovie"  # The name of the operation
get_operation_method = "GET"  # The method of the Operation [GET, POST, PUT, DELETE]
get_operation_expects = None
get_operation_returns = movie_class_.id_  # URI of the object that is returned by the operation
get_operation_returns_header = ["Content-Type", "Content-Length"]
get_operation_expects_header = []
# List of statusCode for the operation
get_operation_status = [HydraStatus(code=200, desc="Movie class returned.")]

delete_operation = "DeleteMovie"  # The name of the operation
delete_operation_method = "DELETE"
delete_operation_expects = movie_class_.id_
delete_operation_returns = None  # URI of the object that is returned by the operation
delete_operation_returns_header = ["Content-Type", "Content-Length"]
delete_operation_expects_header = []
# List of statusCode for the operation
delete_operation_status = [HydraStatus(code=200, desc="Movie class deleted.")]

post = HydraClassOp(update_operation,
                    update_operation_method,
                    update_operation_expects,
                    update_operation_returns,
                    update_operation_expects_header,
                    update_operation_returns_header,
                    update_operation_status)

add = HydraClassOp(add_operation,
                   add_operation_method,
                   add_operation_expects,
                   add_operation_returns,
                   add_operation_expects_header,
                   add_operation_returns_header,
                   add_operation_status)

get = HydraClassOp(get_operation,
                   get_operation_method,
                   get_operation_expects,
                   get_operation_returns,
                   get_operation_expects_header,
                   get_operation_returns_header,
                   get_operation_status)

delete = HydraClassOp(delete_operation,
                      delete_operation_method,
                      delete_operation_expects,
                      delete_operation_returns,
                      delete_operation_expects_header,
                      delete_operation_returns_header,
                      delete_operation_status)

# Adding properties & operation to class
movie_class_.add_supported_prop(movie_name_prop)
movie_class_.add_supported_prop(movie_director_prop)
movie_class_.add_supported_op(post)
movie_class_.add_supported_op(add)
movie_class_.add_supported_op(get)
movie_class_.add_supported_op(delete)

api_doc.add_supported_class(movie_class_)

collection_title = "Movie collection"
collection_name = "MovieCollection"
collection_description = "This collection comprises of all the objects of type Movie"

collection_managed_by = {
    "property": "rdf:type",
    "object": movie_class_.id_,
}
collection_ = HydraCollection(collection_name=collection_name,
                              collection_description=collection_description, manages=collection_managed_by, get=True,
                              post=True)

api_doc.add_supported_collection(collection_)

api_doc.add_baseResource()
api_doc.add_baseCollection()

api_doc.gen_EntryPoint()

doc = api_doc.generate()

if __name__ == "__main__":
    """Print the complete sample Doc in api_doc_output.py."""
    import json
    dump = json.dumps(doc, indent=4, sort_keys=True)
    doc = '''"""Generated MovieApi Documentation sample using api_doc.py"""
    \ndoc = {}\n'''.format(dump)
    # Python does not recognise null, true and false in JSON format, convert
    # them to string
    doc = doc.replace('true', '"true"')
    doc = doc.replace('false', '"false"')
    doc = doc.replace('null', '"null"')
    with open("MovieApi_doc.py", "w") as f:
        f.write(doc)