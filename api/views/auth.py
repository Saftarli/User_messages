from flask_restx import Namespace, Resource, fields
from flask import request
from api.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from api.utils import db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.exceptions import Conflict,BadRequest

auth_namespace = Namespace('auth', description="A namespace for authentication")

signup_model = auth_namespace.model(
    'SignUp', {
        'username': fields.String(required=True, description="A username"),
        'email': fields.String(required=True, description="An email"),
        'password': fields.String(required=True, description="A password"),
    }
)


login_model = auth_namespace.model(
    'Login', {
        'email': fields.String(required=True, description="An email"),
        'password': fields.String(required=True, description="A password"),
    }
)


@auth_namespace.route('/signup')
class SignUp(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(signup_model)
    def post(self):
        """
        Create a new user account
        """
        data = request.get_json()
        # try:
        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password=generate_password_hash(data.get('password')),
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user, HTTPStatus.CREATED
        # except Exception as e:
        #     raise Conflict(f"User with email {data.get('email')} exists")


@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """
        Generate a JWT pair
        """
        data = request.get_json()

        email = data.get('email')
        password= data.get('password')

        user = User.query.filter_by(email=email).first()

        if (user is not None) and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)

            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            return response, HTTPStatus.OK
        raise BadRequest("Invalid User or password")

@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        username = get_jwt_identity()
        access_token = create_access_token(identity=username)

        return {'access_token': access_token}, HTTPStatus.OK
