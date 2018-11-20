from flask_restplus import Namespace, fields

api = api.namespace('api', description='API operations')


eyetrackerRaw = api.model('eytrackerraw',{
    'type': fields.String(required=True, description='type of data', example='raw'),
    'id': fields.String(required=True, description='id of the data', example='FlaskTest'),
    'features':fields.String(required=True, description='List of set of features', example='timestamp,leftX,leftY,rightX,rightY,pupilL,pupilR'),
    'data': fields.String(required=True, description='The dataset that is in need for cleaning', example='1,2,3,4,5,6,7\n7,6,5,nan,3,2,nan')
})






# class EyetrackerResponse:
