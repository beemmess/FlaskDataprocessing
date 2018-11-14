# from flask import Flask, redirect, url_for, request, jsonify
from flask import Flask
from flask_restplus import Api, Resource
from eyetracker import *
app = Flask(__name__)
api = Api(app)

cleaning = api.model('')

@app.route('/eyetracker', methods= ['POST'])
class Eyetracker(Resource):
    def cleaning(self):
        # text = json.dumps(request.json)
        # print(request.json)
        message = request.get_json(silent=True)
        # return Test.testHelloWorld(message)
        return jsonify(Clean.substitution(message))

@app.route('/eyetracker/avgFixationDuration', methods= ['POST'])
def avgFixationDuration():
    # text = json.dumps(request.json)
    # print(request.json)
    message = request.get_json(silent=True)
    # return Test.testHelloWorld(message)
    return jsonify(FeatureExtractin.averageFixationDuration(message))

@app.route('/eyetracker')
def test():
    return "Hello World"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
