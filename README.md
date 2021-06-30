# Flask test

Using Flask to build a Restful API Server with Swagger document.

Integration with Flask-restplus, Flask-Testing, and Flask-SQLalchemy extensions.

## Installation

Install with pip:

```
$ pip install -r requirements.txt
```

## Flask Application Structure
```
zemoga_python_test/
├── templates/                 # view resources
├── tests /                    # tests for the API
├── .gitignore                 # files/directories to ignore
├── config.py                  # params to connections
├── database.py                # manage db connection
├── main.py                    # main file of the application
├── README.md                  # file contains project information
├── requirements.txt           # dependencies of the application
├── routes.py                  # contains all api URLs
└── twitter_auth.py            # twitter connection api
```

## Flask Configuration

#### Example

```
app = Flask(__name__)
app.config['DEBUG'] = True
```
### Configuring From Files

#### Example Usage

```
app = Flask(__name__ )
app.config.from_pyfile('config.Development.cfg')
```

#### cfg example

```
##Flask settings
DEBUG = True  # True/False
TESTING = False

##SWAGGER settings
SWAGGER_DOC_URL = '/api/docs/'
```

## Run Flask
### Run flask for develop
```
$ python main.py
```
In flask, Default port is `5000`

Swagger document page:  `http://127.0.0.1:5000/api/docs/`


## Unittest
```
$ coverage run -m unittest discover
$ coverage report -m
```