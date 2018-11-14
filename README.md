# Python dataprocessing web client
## Introduction
This web client uses Flask, a Python based microframework, as well as the library [Flask-RESTplus](https://flask-restplus.readthedocs.io/en/stable/) as an extension on  Flask. Flask RESTplus makes it easy to create a REST API, the library also includes [Swagger](https://swagger.io/), an open-source framework for documenting REST API's. The soul purpose of this web client is to perform data-processing i.e. cleaning the data, feature extraction etc. The API's routes are formatted to expect JSON strings, these JSON strings carries all the information needed to do certain job for that specific url request.



## Requirements:
To maintain and add to this application there are few things that are required to have to build and run this application.
- Clone this [github repository](https://github.com/beemmess/FlaskDataprocessing)
- Install [Docker](https://www.docker.com/)

*If you are going to test the application outside of docker than you need to*
- Install python 3.5, and the following libraries:

| Library | pip install command |
| ------ | ------ |
| numpy 1.15.2 |  pip install numpy==1.15.2 |
| pandas 0.23.4 | pip install pandas==0.23.4 |
| scikit-learn 0.20.0 | pip install scikit-learn==0.20.0 |
| requests 2.20.0 | pip install requests==2.20.0 |
| Flask 1.0 |  pip install Flask==1.0 |
|flask-restplus 0.12.1|  pip install flask-restplus==0.12.1 |
|scipy 1.1.0|  pip install scipy==1.1.0 |

# Docker
Here below is the Dockerfile that is in the github repository. For this image, ubuntu 18:04 is used, but many other linux version can be used instead.

```dockerfile
# ubuntu 18.04 is the base image
FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

# Create a directory called /app
WORKDIR /app

# Install all the libraries that are in requirements.txt
RUN pip install -r requirements.txt

# "." is the current directory, and then copy everything to /app directory
COPY . /app

# python is the entrypoint when the docker image is ran
ENTRYPOINT [ "python" ]

# app.py is the python script that will run when docker image will run
CMD [ "app.py" ]
```

#### Build and Run
To build and run the docker image then open terminal and go to the cloned directory and endter the following commands.
```sh
$ docker build -t <IMAGE_NAME> .
$ docker run -p 5000:5000 --name <CONTAINER_NAME> <IMAGE_NAME>
```
- . (dot) indicates the current directory
- -p command is used to map the ports <HOST_PORT>:<CONTAINER_PORT>
- --name is used to give the container some name (*optional*)

When the docker image is running than you can head on to [http://localhost:5000/](http://localhost:5000/) which should look something like this:
![SwaggerUI](/images/swaggerUI.png)


# Structure of this application
This library is split into few devices, currently it contains a directory for Tobii eyetracker device, and a director for Shimmer3 GSR+ device.


In the root directory, the ```app.py``` is the main script that will start up the Flask web framework, ```app.py``` also contains all the API routes that will be discussed later on in this documentation. This script below is the skeleton of the ```app.py```. the host is configured to be 0.0.0.0, so as soon as the the web client is running than you can go on to [http://localhost:5000/](http://localhost:5000/)


```py
from flask import Flask, request, jsonify
from flask_restplus import Api, Resource, fields
app = Flask(__name__)

api = Api(app, version='1.0', title='Feature Extraction and cleaning API')
# base namespace is configured to be "api" e.g. http://localhost:5000/api/
api = api.namespace('api', description='API operations')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
```

## New device
here are the step taking in creating a API for a new devices, and lets take the Eyetracker for an example

First create new directory, we will user ```eyetracker``` in this example, then we are going to write a python script in a new file, lets call that ```helloWorld.py```.

we add our new file to the ```__init__.py``` in a ```__all__``` parameter.

```py
__all__ = ("FILE1","FILE2" "....","helloWorld")
```
If we do that, then when we do an import like this ```from eyetracker import *``` then helloWorld will be in this import.
#### Function
in the ```helloWorld.py```, we create a simple function that returns a json message with a "Hello " plus some string that the function recieves in a JSON message.
```py
def helloName(msg):
    name = msg["message"]
    msg["message"] = "Hello {}".format(name)
    return msg
```
Now the function is ready for to be used
#### API route
Next up, we need to add a API route and use that function we just created, therefore, we add a new route in ```app.py``` and a model for the API.


```py
helloModel = api.model('hello',{
    'message': fields.String(required=True, description='example model', example='john')
})
```
helloModel is the the layout of the request, having ```required=True``` which means that this value cant be empty. This model is then added to the ```api.expect``` here below

```py
# for local host:
# http://localhost:5000/api/eyetracker/hello
@api.route('/eyetracker/hello')
class AvgPupilD(Resource):
    @api.doc('helloModel')
    @api.expect(helloModel)
    @api.marshal_with(helloModel, code=200)
    def post(self):
        return helloWorld.helloName(api.payload)
```

This ```api.route``` (http://localhost:5000/api/eyetracker/hello)  is now expecting a JSON string in the format like this:
```
{'message':'Some string'}
```

#### Build and Run
Now we can build the docker image again like descriped earlier in **Docker** section **Build and Run**
