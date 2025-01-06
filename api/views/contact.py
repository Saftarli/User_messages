from flask import jsonify
from flask_restx import Namespace, Resource, fields
from flask import request
from api.models import User,Contact
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from api.utils import db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.exceptions import Conflict,BadRequest

contact_namespace=Namespace('contacts', description="A namespace for contacts")
contact_model = contact_namespace.model(
    'Contact', {
        'id': fields.Integer(),
        'owner_id': fields.Integer(),
        'contact_id': fields.Integer()
    }
)

@contact_namespace.route('/')
class ContactGetandCreated(Resource):
    @contact_namespace.marshal_with(contact_model)
    @jwt_required()
    def get(self):
        tokenden_gelen_username=get_jwt_identity()
        print(tokenden_gelen_username, "%^%^%^%^%^%^%^%^%^%^%^%")
        user=User.query.filter_by(username=tokenden_gelen_username).first()


        """Retrieve contacts."""
        contacts = Contact.query.filter_by(owner_id=user.id).all()  
        # print(contacts, "###$$###$$##$$##$$##$$")
        print(contacts,'&@&@&&@&$&@&@&@&@&&')
        # return contacts, HTTPStatus.OK
        return contacts
    

    @contact_namespace.expect(contact_model)
    @contact_namespace.marshal_with(contact_model)
    @jwt_required()
    def post(self):
        """Create a new contact."""
        tokenden_gelen_username = get_jwt_identity()
        data = request.get_json()
        contact_id = data.get('contact_id')

        # Mövcud istifadəçini token ilə tapırıq
        user = User.query.filter_by(username=tokenden_gelen_username).first()
        if not user:
            return {"message": "User not found"}, HTTPStatus.UNAUTHORIZED

        # Kontaktın mövcudluğunu yoxlayırıq
        contact_user = User.query.get(contact_id)
        if not contact_user:
            return {"message": "Contact user does not exist"}, HTTPStatus.NOT_FOUND

        # Eyni kontaktın artıq mövcud olub-olmadığını yoxlayırıq
        existing_contact = Contact.query.filter_by(owner_id=user.id, contact_id=contact_id).first()
        if existing_contact:
            return {"message": "Contact already exists"}, HTTPStatus.CONFLICT
        

        # Yeni kontakt əlavə edirik
        new_contact = Contact(
            owner_id=user.id,
            contact_id=contact_id
        )
        db.session.add(new_contact)
        db.session.commit()

        return new_contact, HTTPStatus.CREATED
    
@contact_namespace.route('/<int:contact_id>')
class ContactDeleteandEdit(Resource):

    @jwt_required()
    @contact_namespace.marshal_with(contact_model)
    def delete(self, contact_id):
        """
        Delete an order wit
        """

        contact_to_delete=Contact.get_by_id(contact_id)

        db.session.delete(contact_to_delete)
        

        return contact_to_delete, HTTPStatus.OK
    








# Userlər arasında mesajlaşma sistemi
# -userlər qeydiyyat və login ola bilməlidir(jwt) ok
# -hər userin hesabında kontaktları olmalıdır.ok
# -user login olubsa, kontaktlarındakı userlərə msj gondərə bilməlidir. 
# -user göndərdiyi msj-ı gondərdiyi zamandan 1 dəq sonraya kimi editləyə bilər, əgər 1 dəqiqəni keçibsə editləmə mümkün olmamalıdır
# -həmçinin user göndərdiyi msjı göndərdiyi zamandan 1 dəq sonraya kimi silə bilər.(gmaildəki unsend kimi)1 dəqiqəni keçdisə delete mümkün olmamalıdır
# -user contactına mövcud olan userlərdən kimisə artıra bilər ok
# -user contactındakı hər hansı öz contactından silə bilər ok
# -user ona gələn bütün mesajlara baxa bilər
# -user ona hər hansı bir contactdan gələn mesajlara baxa bilər
# -user contactındakı mesajları silə bilər