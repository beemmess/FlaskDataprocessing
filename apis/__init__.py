from flask_restplus import Api

from .eyetrackerNamespace import api as eyetrackerNs
from .shimmerNamespace import api as shimmerNs
# ....
# .... add and import additional namespaces as needed
# from .{device}Namespace import api as {device}Ns


api = Api(
    title='Data Processing Web Service',
    version='1.0',
    description='Feature Extraction and cleaning API',
    # All API metadatas
)

api.add_namespace(eyetrackerNs)
api.add_namespace(shimmerNs)
# ...
# ... add additional namespace to api as needed
# api.add_namespace({device}Ns)
