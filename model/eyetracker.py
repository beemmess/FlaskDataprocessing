#
# raw = api.model('raw',{
#     'type': fields.String(required=True, description='type of data', example='raw'),
#     'id': fields.String(required=True, description='id of the data', example='FlaskTest'),
#     'features':fields.String(required=True, description='List of set of features', example='timestamp,leftX,leftY,rightX,rightY,pupilL,pupilR'),
#     'data': fields.String(required=True, description='The dataset that is in need for cleaning', example='1,2,3,4,5,6,7\n7,6,5,nan,3,2,nan')
# })
# # Response
# preprocessed = api.model('preprocessed',{
#     'type': fields.String(required=True, description='type of data', example='preprocessed'),
#     'id': fields.String(required=True, description='id of the data', example='FlaskTest'),
#     'features':fields.String(required=True, description='List of set of features', example='timestamp,leftX,leftY,rightX,rightY,pupilL,pupilR'),
#     'data': fields.String(required=True, description='The dataset that is in need for cleaning', example='1,2,3,4,5,6,7\n7,6,5,6,3,2,2')
# })
#
# # Response
# avgPupil = api.model('avgPupil',{
#     'type': fields.String(required=True, description='type of data', example='avgPupil'),
#     'id': fields.String(required=True, description='id of the data', example='FlaskTest'),
#     'features':fields.String(required=True, description='List of features', example='pupilL,pupilR'),
#     'data': fields.String(required=True, description='Average pupil Diameter',example='1,2')
# })
