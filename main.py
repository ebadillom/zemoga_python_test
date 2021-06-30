from flask import Flask, make_response, jsonify

from api_spec import spec
from config import DB_USER, DB_PASSWORD, DB_NAME, DB_SERVER
from database import mysql
from routes import portfolio
from swagger import swagger_ui_blueprint, SWAGGER_URL

# instance of server
app = Flask(__name__)

# connect to database
app.config['MYSQL_DATABASE_USER'] = DB_USER
app.config['MYSQL_DATABASE_PASSWORD'] = DB_PASSWORD
app.config['MYSQL_DATABASE_DB'] = DB_NAME
app.config['MYSQL_DATABASE_HOST'] = DB_SERVER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
mysql.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def custom400(error):
    return make_response(jsonify({'message': error.description}), 400)


# register blueprint
app.register_blueprint(portfolio)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

with app.test_request_context():
    # register all swagger documented functions here
    for fn_name in app.view_functions:
        if fn_name == 'static':
            continue
        print(f"Loading swagger docs for function: {fn_name}")
        view_fn = app.view_functions[fn_name]
        spec.path(view=view_fn)


@app.route("/api/swagger.json")
def create_swagger_spec():
    return jsonify(spec.to_dict())


if __name__ == '__main__':
    app.run(debug=True)
