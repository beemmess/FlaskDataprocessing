# Python data-processing web client
## Introduction
This web client uses Flask, a Python-based microframework, as well as the library [Flask-RESTplus](https://flask-restplus.readthedocs.io/en/stable/) as an extension on  Flask. Flask RESTplus makes it easy to create a REST API; the library also includes [Swagger](https://swagger.io/), an open-source framework for documenting REST API's. The sole purpose of this web client is to perform data-processing, i.e. cleaning the data, feature extraction etc. The API's routes are formatted to expect JSON strings; these JSON strings carries all the information needed to do a certain job for that specific URL request.



## Requirements:
To maintain and add to this application there are a few things that are required to have to build and run this application.
- Clone this [github repository](https://github.com/beemmess/FlaskDataprocessing)
- Install [Docker](https://www.docker.com/)

*If you are going to test/run some parts of the functions in the library outside of docker than you need to install some or all of the below libraries, depanding on which part of the library you are going to test/run*
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
Here below is the Dockerfile that is in the GitHub repository. For this image, ubuntu 18:04 is used, but many other Linux version can be used instead.

```dockerfile
# Ubuntu 18.04 is the base image
FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

# Create a directory called /app
WORKDIR /app

# Install all the libraries that are in requirements.txt
RUN pip install -r requirements.txt

# "." is the current directory, and then copy everything to the /app directory
COPY . /app

# python is the entry point when the docker image is ran
ENTRYPOINT [ "python" ]

# app.py is the python script that will run when docker image will run
CMD [ "app.py" ]
```

#### Build and Run
To build and run the docker image then open a terminal and go to the directory of the cloned repository and enter the following commands.
```sh
$ docker build -t <IMAGE_NAME> .
$ docker run -p 5000:5000 --name <CONTAINER_NAME> <IMAGE_NAME>
```
- . (dot) indicates the current directory
- -p command is used to map the ports <HOST_PORT>:<CONTAINER_PORT>
- --name is used to give the container some name (*optional*)

When the docker image is running then you can head on to [http://localhost:5000/](http://localhost:5000/) which should look something like this:
![SwaggerUI](/images/Swagger.png)
This is Swagger UI, from here you can test the API by performing requests by choosing the desired route. Each route has an example JSON string that can be used for testing the requests.

# Directory Structure


```bash
 project/
   ├── __init__.py
   ├── app.py     
   ├── dockerfile
   ├── apis/      # Main API's entry points
   │   ├── __init__.py
   │   ├── eyetrackerNamespace.py
   │   ├── shimmerNamespace.py
   │   ├── ...
   │   └── [device]Namespace.py
   │
   └── core/      # Business logic
       ├── __init__.py
       ├── eyetracker/
       │   ├── __init__.py
       │   ├── Clean.py
       │   ├── EyetrackerFx.py
       │   └── ...
       │
       ├── shimmer/
       │   ├── __init__.py
       │   ├── ShimmerFx.py
       │   └── ...
       │
       └── .../
           ├── __init__.py
           └── ...       
```
This application scales pretty well, the structure is organized so that only few things are needed to be done to add new API routes and business logic. If you follow the Step-By-Steb guide later on, then the new namespace is only needed to be imported and added to the list in `apis/__init__.py` as seen here in the script below.

```py
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
```


### Edit/Add new things to the application
The business logic is split into few devices; currently it contains a directory for Tobii eye tracker device and a director for Shimmer3 GSR+ device.

In the root directory, the `app.py` is the main script that will start up the Flask web framework, `app.py` also imports the `api` from `apis/__init__.py`  which cointans all the all the API routes. The host is configured to be `0.0.0.0` therefore, when the web client is running then you can go on to [http://localhost:5000/](http://localhost:5000/) and try it out.

```py
from flask import Flask
from apis import api

app = Flask(__name__)
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
```

# Step-by-step
Here is a step-by-step guide to implement a new device or add new business logic to an already defined device. Now, let's use the eye tracker and add a new logic to it.

#### Step 0
When adding a new device, then create a new business logic directory for that particular device, similar to shimmer and eye tracker and add that directory in `core/` along with a `__init__py` file.

#### Step 1
We are going to add a new file to the `core/eyetracker/` directory, and lets call that `helloWorld.py` later on, we will add some business logic to it.

#### Step 2
In the `helloWorld.py` we create a simple function that returns a message with a "Hello " plus some string that the function receives in a JSON message from the `api.payload` (in step 3)
```py
def helloName(msg):
    name = msg["message"]
    msg["message"] = "Hello {}".format(name)
    return msg
```
Now the function is ready to be used
#### Step 3

Next up, we need to add an API route to use that function we just created. Therefore, we add a new route to `apis/eyetrackerNamespace.py` and a model for the API, ` @api.route('/eyetracker/hello') ` defines the route to that particular function.

```py
helloModel = api.model('hello',{
    'message': fields.String(required=True, description='example model', example='john')
})
```
`helloModel` is the layout of the request, having `required=True` which means that this value cant be empty. This model is then added to the `api.expect` as seen here below

```py
from core.eyetracker import helloWorld # import helloWorld from the module core/eyetracker/

@api.route('/eyetracker/hello')   
class hello(Resource):            
    @api.doc('helloModel')        
    @api.expect(helloModel)
    @api.marshal_with(helloModel, code=200)
    def post(self):
        # JSON string is gotten by getting the api payload
        return helloWorld.helloName(api.payload)
```
As you can see the ` @api.marshal_with ` decorator is also used, this decorator documents the methods and a optional parameter code allows you to specify the expected HTTP status code (200 by default). Now, This `api.route` (http://localhost:5000/eyetracker/hello)  is now expecting a JSON string in the format like this:
```
{'message':'Some string'}
```

#### Step 4
If this is a new device, then we need to import and add the namespace to `apis/__init__.py`

```py
api.add_namespace(eyetrackerNs)
api.add_namespace(shimmerNs)
# ...
# ... add additional namespace to api as needed
# api.add_namespace({device}Ns)
```

#### Step 5
Now we can build the docker image again like described earlier in **Docker** section: **Build and Run**

# More Information
### SwaggerUI and API documentation

Swagger API documentation is automatically generated and available from the API’s root URL, as seen on the image here above, which is an auto generated Swagger UI. You can configure the documentation using the ``` @api.doc()``` decorator [[1]](https://flask-restplus.readthedocs.io/en/stable/swagger.html). The ``` @api.expect() ``` decorator allows you to specify the expected input fields[[2]](https://flask-restplus.readthedocs.io/en/stable/swagger.html#the-api-marshal-with-decorator). The ``` @api.response() ``` decorator allows you to document the known responses and is a shortcut for ``` @api.doc(responses='...') ``` [[3]](https://flask-restplus.readthedocs.io/en/stable/swagger.html#documenting-with-the-api-response-decorator). You can provide class-wide documentation using the doc parameter of Api.route(). This parameter accepts the same values as the ```Api.doc()``` decorator[[4]](https://flask-restplus.readthedocs.io/en/stable/swagger.html#the-api-route-decorator). For example, these two declarations are equivalent:

Using ``` @api.doc() ```:
```py
@api.route('/my-resource/<id>', endpoint='my-resource')
@api.doc(params={'id': 'An ID'})
class MyResource(Resource):
    def get(self, id):
        return {}
```
Using ``` @api.route() ```:

```py
@api.route('/my-resource/<id>', endpoint='my-resource', doc={'params':{'id': 'An ID'}})
class MyResource(Resource):
    def get(self, id):
        return {}
```

For more information and documentation, please visit the [Flask RESTplus documentation](https://flask-restplus.readthedocs.io/en/stable/swagger.html).


### Links

| Name | Website |
| ------ | ------ |
| Flask|  http://flask.pocoo.org/ |
| Flask RESTplus | https://flask-restplus.readthedocs.io/en/stable/ |
| Swagger | https://swagger.io/|
| Docker | https://www.docker.com/|

# Authors
- Bjarki Mar Stefansson - Initial work
- Barbara Weber - Supervisor
