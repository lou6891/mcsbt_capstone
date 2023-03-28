# Import required packages
from mongoDB_call import get_collection, login
from mongoDB_post import register
from flask import Flask, jsonify, make_response, request
from flask_restx import Api, Namespace, Resource, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, create_refresh_token
import datetime
import re
import hashlib
from mongoDb_load_data import collections_verifies_uploader

# Uncomment the following line if you want to verify and upload collections to the database
# collections_verifies_uploader()

########################################################################################################################
# ############### API API API API API API API API API API API API API API API API API  API API API API ############### #
########################################################################################################################


# Initialize the Flask application and configure the JWT secret key
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'pepe-is-the-best'  # Change this to a long random string in production
jwt = JWTManager(app)

# Configure the API and its authorizations
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': ''' Bearer token, created at login or registration, to make this authorization work,
                       get the token from login, and then insert "Bearer your_token"''',
    }
}

api = Api(app,
          version='1.0',
          title='Final Capstone Project API',
          description="""
              This RESTS API is an API built with FLASK
              and FLASK-RESTX libraries
          """,
          contact="Luca Conti",
          endpoint="/api/v1",
          authorizations=authorizations
          )

# Set up a request parser for username and password arguments
auth_parser = reqparse.RequestParser()
auth_parser.add_argument('username', type=str, help='username')
auth_parser.add_argument('password', type=str, help='password')

# Set up a request parser for the limit argument
limit_parser = reqparse.RequestParser()
limit_parser.add_argument('limit', type=int, default=1000)


def is_sha256_hash(s):
    """Checks if the given string is a SHA256 hash
    This function is used so that if the user is using the swagger UI,
    the api will hash the password in login and registration to keep the database consistent
    """
    return bool(re.match(r'^[a-f0-9]{64}$', s))


########################################################################################################################
# #################                                    ARTICLES                                      ################# #
########################################################################################################################
# Namespace for articles
articles = Namespace('Articles',
                     description='API endpoint related to the Article DB',
                     path='/api/v1')
api.add_namespace(articles)


# Resource to get all articles
@articles.route("/articles")
class GetAllArticles(Resource):
    @api.doc(parser=limit_parser,
             security='Bearer Auth',
             description='''
             API endpoint in charge of retrieving all data related to the articles, 
             limit set by default to 1000 rows.
             ''')
    @jwt_required()
    def get(self):
        args = limit_parser.parse_args()
        limit = args['limit']
        db_call = get_collection("articles", limit)

        if db_call:
            return make_response(jsonify({'result': [dict(row) for row in db_call]}), 201)
        else:
            return make_response(jsonify({'result': "Error in DB call"}), 404)


########################################################################################################################
# #################                                  TRANSACTIONS                                    ################# #
########################################################################################################################

# Namespace for transactions
transactions = Namespace('transactions',
                         description='API endpoint related to the Transactions DB',
                         path='/api/v1')
api.add_namespace(transactions)


# Resource to get all transactions
@transactions.route("/transactions")
class GetAllTransactions(Resource):
    @api.doc(parser=limit_parser,
             security='Bearer Auth',
             description='''
             API endpoint in charge of retrieving all data related to the transactions, 
             limit set by default to 1000 rows.
             ''')
    @jwt_required()
    def get(self):
        args = limit_parser.parse_args()
        limit = args['limit']
        db_call = get_collection("transactions", limit)

        if db_call:
            return make_response(jsonify({'result': [dict(row) for row in db_call]}), 201)
        else:
            return make_response(jsonify({'result': "Error in DB call"}), 404)


# Namespace for customers
customers = Namespace('customers',
                      description='API endpoint related to the Customers DB',
                      path='/api/v1')
api.add_namespace(customers)


########################################################################################################################
# #################                                   CUSTOMERS                                      ################# #
########################################################################################################################


# Resource to get all customers
@customers.route("/customers")
class GetAllCustomers(Resource):
    @api.doc(parser=limit_parser,
             security='Bearer Auth',
             description='''
             API endpoint in charge of retrieving all data related to the customers, 
             limit set by default to 1000 rows.
             ''')
    @jwt_required()
    def get(self):
        args = limit_parser.parse_args()
        limit = args['limit']
        db_call = get_collection("customers", limit)

        if db_call:
            return make_response(jsonify({'result': [dict(row) for row in db_call]}), 201)
        else:
            return make_response(jsonify({'result': "Error in DB call"}), 404)


########################################################################################################################
# #################                              USERS USERS USERS USERS                             ################# #
########################################################################################################################


# Namespace for users
users = Namespace('users',
                  description='User login, registration and token refresh',
                  path='/api/v1')
api.add_namespace(users)


# Resource for user login
@users.route("/users/login/")
class GetUser(Resource):
    @api.doc(parser=auth_parser,
             description='''
             API endpoint in charge of login, it checks if the user is present in the DB,
             If positive it return the access and refresh token needed for login
             ''')
    def post(self):
        args = auth_parser.parse_args()
        username = args['username']
        password = args['password']

        # Check if password is hashed (i.e.: coming from client), if not hash it to keep db consistency
        if not is_sha256_hash(password):
            password = hashlib.sha256(password.encode()).hexdigest()

        db_call = login(username, password)

        if db_call:
            # Generate access and refresh tokens
            token_timedelta = 5
            access_token_expires_in = datetime.timedelta(minutes=token_timedelta)
            access_token = create_access_token(identity=username, expires_delta=access_token_expires_in)

            refresh_token_timedelta = 30
            refresh_token_expires_in = datetime.timedelta(days=refresh_token_timedelta)
            refresh_token = create_refresh_token(identity=username, expires_delta=refresh_token_expires_in)

            return jsonify({"result": db_call, "token": access_token, "token_timedelta": token_timedelta,
                            "refresh_token": refresh_token, "refresh_token_timedelta": refresh_token_timedelta})
        else:
            return make_response(jsonify({"result": "User not found"}), 404)


# Resource for user registration
@users.route("/users/register/")
class CreateUser(Resource):
    @api.doc(parser=auth_parser,
             description='''
             API endpoint in charge of registering the user in the DB, if registration is completed successfully, 
             or the user already exists in the systems,it return the access and refresh token needed for login
             ''')
    def post(self):
        args = auth_parser.parse_args()
        username = args['username']
        password = args['password']

        # Check if password is hashed (i.e.: coming from client), if not hash it to keep db consistency
        if not is_sha256_hash(password):
            password = hashlib.sha256(password.encode()).hexdigest()

        db_call = register(username, password)

        if db_call:
            # Generate access and refresh tokens
            token_timedelta = 5
            access_token_expires_in = datetime.timedelta(minutes=token_timedelta)
            access_token = create_access_token(identity=username, expires_delta=access_token_expires_in)

            refresh_token_timedelta = 30
            refresh_token_expires_in = datetime.timedelta(days=refresh_token_timedelta)
            refresh_token = create_refresh_token(identity=username, expires_delta=refresh_token_expires_in)

            return jsonify({"result": db_call, "token": access_token, "token_timedelta": token_timedelta,
                            "refresh_token": refresh_token, "refresh_token_timedelta": refresh_token_timedelta, })
        else:
            return jsonify({"result": "Error in creating the user"})


# Resource for refreshing access tokens
@users.route("/users/refresh/")
class RefreshToken(Resource):
    @jwt_required(refresh=True)
    @api.doc(description='''
                 API endpoint in charge of refreshing the user bearer token, the token has validity of 5 minuted,
                 automatically refreshed by the client using the refresh token
                 ''')
    def post(self):
        current_user = get_jwt_identity()

        token_timedelta = 5
        access_token_expires_in = datetime.timedelta(minutes=token_timedelta)
        access_token = create_access_token(identity=current_user, expires_delta=access_token_expires_in)

        if access_token:
            return jsonify({"token": access_token, "token_timedelta": token_timedelta})
        else:
            return make_response(jsonify({"result": "Error in generating refresh token"}), 404)


########################################################################################################################


if __name__ == '__main__':
    app.run(debug=True)
