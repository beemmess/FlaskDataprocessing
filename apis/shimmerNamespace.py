from flask_restplus import Namespace, Resource, fields
from core.shimmer import ShimmerFx

api = Namespace('shimmer', description='Shimmer related operations')

# expect
shimmerRaw = api.model('shimmerraw',{
    'type': fields.String(required=True, description='type of data', example='raw'),
    'id': fields.String(required=True, description='id of the data', example='FlaskTest'),
    'apiUrl': fields.String(required=True, description='api url locations', example='some/ending/of/url'),
    'device': fields.String(required=True, description='name of the device/data', example='shimmer'),
    'attributes':fields.String(required=True, description='List of set of attributes', example='timestamp,GSR,PPG,task'),
    'data': fields.String(required=True, description='The dataset that is in need for processing', example='1,2,3,1\n4,5,6,1')
})

# response
shimmerNormalized = api.model('normGsrAndPpg',{
    'type': fields.String(required=True, description='type of data', example='normalized'),
    'apiUrl': fields.String(required=True, description='api url locations', example='some/ending/of/url'),
    'device': fields.String(required=True, description='name of the device/data', example='shimmer'),
    'id': fields.String(required=True, description='id of the data', example='FlaskTest'),
    'attributes':fields.String(required=True, description='List of set of attributes', example='timestamp,GSR,PPG,task'),
    'data': fields.String(required=True, description='The dataset that is in need for processing', example='1,1.003,1.004,1')
})

# response
shimmerAvg = api.model('avgGSRandPPG',{
    'type': fields.String(required=True, description='type of data', example='avgGSRandPPG'),
    'apiUrl': fields.String(required=True, description='api url locations', example='some/ending/of/url'),
    'device': fields.String(required=True, description='name of the device/data', example='shimmer'),
    'id': fields.String(required=True, description='id of the data', example='FlaskTest'),
    'attributes':fields.String(required=True, description='List of set of attributes', example='avgGSR,avgPPG'),
    'data': fields.String(required=True, description='The dataset that is in need for processing', example='1800,1900')
})


@api.route('/normalize')
class shimmerNormalize(Resource):
    @api.doc('normalizeShimmer')
    @api.expect(shimmerRaw)
    @api.marshal_with(shimmerNormalized, code=200)
    def post(self):
        return ShimmerFx.normalize(api.payload)

@api.route('/avgGSRandPPG')
class avgShimmer(Resource):
    @api.doc('normalizeShimmer')
    @api.expect(shimmerRaw)
    @api.marshal_with(shimmerAvg, code=200)
    def post(self):
        return ShimmerFx.avgGSRandPPG(api.payload)
