from flask import jsonify
from flask_restx import Namespace, Resource, fields
from flask import request
from api.models import User,Contact,Message
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from api.utils import db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.exceptions import Conflict,BadRequest
from datetime import datetime as dt , timedelta
from sqlalchemy import DateTime 


messages_namespace=Namespace('messages', description='A Namspace for messages')
message_model = messages_namespace.model('Message', {
    'id': fields.Integer,
    'sender_id': fields.Integer,
    'recipient_id': fields.Integer,
    'timestamp': fields.DateTime,
    'content': fields.String,
    
})

# @messages_namespace.route('/')
# class GetMessages(Resource):
#     @messages_namespace.marshal_with(message_model)
#     @jwt_required()
#     def get(self):
#         current_user_username = get_jwt_identity()
#         loginned_username = User.query.filter_by(username = current_user_username).first()
#         messages = Message.query.filter_by(recipient_id=loginned_username.id).all()
#         return messages

@messages_namespace.route('/<int:user_id>')
class MessagesSend(Resource):
    @messages_namespace.expect(message_model)
    # @messages_namespace.marshal_with(message_model)
    @jwt_required()
    def post(self, user_id):
        username = get_jwt_identity()
        sender_user = User.query.filter_by(username=username).first()
        recipient_user = User.query.filter_by(id = user_id).first()
        contacts = Contact.query.filter_by(owner_id=sender_user.id).all()
        print(contacts, '$%$%#^#&$&#&&$&*$^#^#^&@^@^&@&^@')
        if recipient_user not in contacts:
            new_message = {
                "Cavab": "recipient contactinda yoxdur"
            }
            response = new_message, HTTPStatus.BAD_REQUEST
            # return new_message, HTTPStatus.BAD_REQUEST, 404
        else:
            data = request.json
            content = data.get('content')
            new_message = Message(
            sender_id = sender_user.id,
            recipient_id = recipient_user.id,
            content = data.get('content')),
                                

            db.session.add(new_message)
            db.session.commit()
            response = new_message, HTTPStatus.CREATED
        return response
    
    @messages_namespace.expect(message_model)
    @jwt_required()
    def get(self,user_id):
        username = get_jwt_identity()
        sender_user = User.query.filter_by(username=username).first()
        recipient_user = User.query.filter_by(id = user_id).first()
        messages = Message.query.filter_by(sender_id = sender_user.id,
                                           recipient_id=recipient_user.id).all()
        
        return messages, HTTPStatus.OK

@messages_namespace.route('/inbox')
class MessageInbox(Resource):
    @messages_namespace.marshal_with(message_model)
    @jwt_required()
    def get(self):
        username = get_jwt_identity()
        loggined_user = User.query.filter_by(username=loggined_user).first()
        messages = Message.query.filter_by(recipient_id = loggined_user.id)

        return messages, HTTPStatus.OK


@messages_namespace.route('/<int:messages_id>')
class MessageDelete(Resource):
    @messages_namespace.marshal_with(message_model)
    @jwt_required()
    def delete(self, messages_id):
        username = get_jwt_identity()
        loggined_user = User.query.filter_by(username=loggined_user).first()
        inbox_messages = Message.query.filter_by(recipient_id = loggined_user.id)
        delete_message = Message.query.filter_by(id=messages_id).first()
        if delete_message is not None and delete_message in inbox_messages:
            delete_message.delete()

        return delete_message, HTTPStatus.NO_CONTENT
    
    @messages_namespace.marshal_with(message_model)
    @jwt_required()
    def patch(self, messages_id):
        username = get_jwt_identity()
        loggined_user = User.query.filter_by(username= loggined_user).first()
        inbox_messages = Message.query.filter_by(recipient_id = loggined_user.id)
        update_message = Message.query.filter_by(id=messages_id).first()
        if update_message is not None and update_message in inbox_messages:
            xtime = dt.utcnow - update_message.timestamp
            if xtime <= timedelta(minutes=1):
                data = messages_namespace.payload
                update_message.content = data['content']

                db.session.commit()
                
                return update_message, HTTPStatus.OK    

            else:
                response = {
                    "body": "Mesaji deyise bilmersen upss"
                }






