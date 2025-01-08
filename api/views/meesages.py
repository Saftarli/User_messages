from flask import jsonify
from flask_restx import Namespace, Resource, fields
from flask import request
from api.models import User,Contact,Message
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from api.utils import db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.exceptions import Conflict,BadRequest

messages_namespace=Namespace('messages', description='A Namspace for messages')
message_model = messages_namespace.model('Message', {
    'id': fields.Integer,
    'sender_id': fields.Integer,
    'recipient_id': fields.Integer,
    'timestamp': fields.DateTime,
    'content': fields.String,
    'status': fields.String
})

@messages_namespace.route('/')
class GetMessages(Resource):
    @messages_namespace.marshal_with(message_model)
    @jwt_required()
    def get(self):
        current_user_username = get_jwt_identity()
        loginned_username = User.query.filter_by(username = current_user_username).first()
        messages = Message.query.filter_by(recipient_id=loginned_username.id).all()
        return messages

@messages_namespace.route('/int:user_id')
class MessagesSend(Resource):
    @messages_namespace.expect(message_model)
    @messages_namespace.marshal_with(message_model)
    @jwt_required()
    def post(self, user_id):
        username = get_jwt_identity()
        sender_user = User.query.filter_by(username=username).first()
        recipient_user = User.query.filter_by(id = user_id)
        data = request.json
        print(username, "#$#$#$#$#$#$$$#$#")
        # new_message = Message(
        #     sender_id = sender_user.id,
        #     recipient_id = recipient_user.id,
        #     content = 

        # )
    
    
