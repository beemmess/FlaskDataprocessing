from flask_restplus import Namespace, Resource, fields

from core.eyetracker import Clean, EyetrackerFx, helloWorld

api = Namespace('eyetracker', description='Eyetracker related operations')

# expect
eyetrackerRaw = api.model('eytrackerraw',{
    'type': fields.String(required=True, description='type of data', example='raw'),
    'id': fields.String(required=True, description='id of the data', example='FlaskTest'),
    'features':fields.String(required=True, description='List of set of features', example='timestamp,leftX,leftY,rightX,rightY,pupilL,pupilR,task'),
    'data': fields.String(required=True, description='The dataset that is in need for cleaning', example='1,2,3,4,5,6,7,SomeTask1\n7,6,5,nan,3,2,nan,SomeTask2')
})
# Response
preprocessed = api.model('preprocessed',{
    'type': fields.String(required=True, description='type of data', example='preprocessed'),
    'id': fields.String(required=True, description='id of the data', example='FlaskTest'),
    'features':fields.String(required=True, description='List of set of features', example='timestamp,leftX,leftY,rightX,rightY,pupilL,pupilR,task'),
    'data': fields.String(required=True, description='The dataset that is in need for cleaning', example='1,2,3,4,5,6,7,someTask1\n7,6,5,6,3,2,2,someTask2')
})

# Response
substition = api.model('substition',{
    'type': fields.String(required=True, description='type of data', example='substition'),
    'id': fields.String(required=True, description='id of the data', example='FlaskTest'),
    'features':fields.String(required=True, description='List of set of features', example='timestamp,leftX,leftY,rightX,rightY,pupilL,pupilR,task'),
    'data': fields.String(required=True, description='The dataset that is in need for cleaning', example='1,2,3,4,5,6,7,someTask1\n7,6,5,6,3,2,2,someTask2')
})

# Response
interpolate = api.model('interpolate',{
    'type': fields.String(required=True, description='type of data', example='interpolate'),
    'id': fields.String(required=True, description='id of the data', example='FlaskTest'),
    'features':fields.String(required=True, description='List of set of features', example='timestamp,leftX,leftY,rightX,rightY,pupilL,pupilR,task'),
    'data': fields.String(required=True, description='The dataset that is in need for cleaning', example='1,2,3,4,5,6,7,someTask1\n7,6,5,6,3,2,2,someTask2')
})

# Response
avgPupil = api.model('avgPupil',{
    'type': fields.String(required=True, description='type of data', example='avgPupil'),
    'id': fields.String(required=True, description='id of the data', example='FlaskTest'),
    'features':fields.String(required=True, description='List of features', example='pupilL,pupilR'),
    'data': fields.String(required=True, description='Average pupil Diameter',example='1,2')
})



@api.route('/substitution')
class Eyetracker(Resource):
    @api.doc('substituion_cleaning')
    @api.expect(eyetrackerRaw)
    @api.marshal_with(substition, code=200)
    def post(self):
        return Clean.substitution(api.payload)

@api.route('/interpolate')
class Eyetracker(Resource):
    @api.doc('substituion_cleaning')
    @api.expect(eyetrackerRaw)
    @api.marshal_with(interpolate, code=200)
    def post(self):
        return Clean.interpolateMissingData(api.payload)

# TODO: change expect
@api.route('/avgPupil')
class AvgPupilD(Resource):
    @api.doc('pupil_avg')
    @api.expect(preprocessed)
    @api.marshal_with(avgPupil, code=200)
    def post(self):
        return EyetrackerFx.averagePupilDiameter(api.payload)




# Simple api route for demonstration purpose and for step-by-step guide
helloModel = api.model('hello',{
    'message': fields.String(required=True, description='example model', example='john')
})

@api.route('/hello')
class hello(Resource):
    @api.doc('helloModel')
    @api.expect(helloModel)
    @api.marshal_with(helloModel, code=200)
    def post(self):
        return helloWorld.helloName(api.payload)
