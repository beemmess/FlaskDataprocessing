# from flask import Flask, redirect, url_for, request, jsonify

# documentation
# https://flask-restplus.readthedocs.io/en/stable/api.html

from flask import Flask, request, jsonify
from flask_restplus import Api, Resource, fields
from eyetracker import *
from shimmer import ShimmerFx
from model import *
app = Flask(__name__)
api = Api(app, version='1.0', title='Feature Extraction and cleaning API')

api = api.namespace('api', description='API operations')

# expect
eyetrackerRaw = api.model('eytrackerraw',{
    'type': fields.String(required=True, description='type of data', example='raw'),
    'id': fields.String(required=True, description='id of the data', example='FlaskTest'),
    'features':fields.String(required=True, description='List of set of features', example='timestamp,leftX,leftY,rightX,rightY,pupilL,pupilR'),
    'data': fields.String(required=True, description='The dataset that is in need for cleaning', example='1,2,3,4,5,6,7\n7,6,5,nan,3,2,nan')
})
# Response
preprocessed = api.model('preprocessed',{
    'type': fields.String(required=True, description='type of data', example='preprocessed'),
    'id': fields.String(required=True, description='id of the data', example='FlaskTest'),
    'features':fields.String(required=True, description='List of set of features', example='timestamp,leftX,leftY,rightX,rightY,pupilL,pupilR'),
    'data': fields.String(required=True, description='The dataset that is in need for cleaning', example='1,2,3,4,5,6,7\n7,6,5,6,3,2,2')
})

# Response
avgPupil = api.model('avgPupil',{
    'type': fields.String(required=True, description='type of data', example='avgPupil'),
    'id': fields.String(required=True, description='id of the data', example='FlaskTest'),
    'features':fields.String(required=True, description='List of features', example='pupilL,pupilR'),
    'data': fields.String(required=True, description='Average pupil Diameter',example='1,2')
})

# expect
shimmerRaw = api.model('shimmerraw',{
    'type': fields.String(required=True, description='type of data', example='raw'),
    'id': fields.String(required=True, description='id of the data', example='FlaskTest'),
    'features':fields.String(required=True, description='List of set of features', example='timestamp,GSR,PPG'),
    'data': fields.String(required=True, description='The dataset that is in need for processing', example='1,2,3\n4,5,6')
})

# response
shimmerAvg = api.model('avgGSRandPPG',{
    'type': fields.String(required=True, description='type of data', example='avgGSRandPPG'),
    'id': fields.String(required=True, description='id of the data', example='FlaskTest'),
    'features':fields.String(required=True, description='List of set of features', example='timestamp,avgGSR,avgPPG'),
    'data': fields.String(required=True, description='The dataset that is in need for processing', example='1,3.5,4.5')
})





@api.route('/eyetracker/substitution')
class Eyetracker(Resource):
    @api.doc('substituion_cleaning')
    @api.expect(eyetrackerRaw)
    @api.marshal_with(preprocessed, code=200)
    def post(self):
        return Clean.substitution(api.payload)


@api.route('/eyetracker/avgPupil')
class AvgPupilD(Resource):
    @api.doc('pupil_avg')
    @api.expect(preprocessed)
    @api.marshal_with(avgPupil, code=200)
    def post(self):
        return EyetrackerFx.averagePupilDiameter(api.payload)

@api.route('/shimmer/avg')
class AvgPupilD(Resource):
    @api.doc('shimmer_avg')
    @api.expect(shimmerRaw)
    @api.marshal_with(shimmerAvg, code=200)
    def post(self):
        return ShimmerFx.avgGSRandPPG(api.payload)


# Simple api route for demonstration purpose and for step-by-step guide
helloModel = api.model('hello',{
    'message': fields.String(required=True, description='example model', example='john')
})

@api.route('/eyetracker/hello')
class hello(Resource):
    @api.doc('helloModel')
    @api.expect(helloModel)
    @api.marshal_with(helloModel, code=200)
    def post(self):
        return helloWorld.helloName(api.payload)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
