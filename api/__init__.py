from flask import Flask
from flask_restx import Api
from .config.config import config_dict
from api.utils import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound,MethodNotAllowed
from api.models import User, Contact
from api.views.auth import auth_namespace
from api.views.contact import contact_namespace

def create_app(config=config_dict['dev']):
    app=Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    migrate=Migrate(app,db)

    jwt=JWTManager(app) 

    api = Api(app)

    # api.add_namespace()
    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(contact_namespace, path='/contacts')

    
    # @api.errorhandler(NotFound)
    # def not_found(error):
    #     return{"error": "Not Found"},404
    
    # @api.errorhandler(MethodNotAllowed)
    # def method_not_allowed(error):
    #     return {"error": "Method Not Allowed"},405

    @app.shell_context_processor
    def make_shell_context():
        return{
            'db':db,
            'User':User,
            'Contact': Contact
        }

    return app 