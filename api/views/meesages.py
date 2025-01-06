from flask import jsonify
from flask_restx import Namespace, Resource, fields
from flask import request
from api.models import User,Contact
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from api.utils import db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.exceptions import Conflict,BadRequest

messages_namespace=Namespace('messages', description='A Namspace for messages')

