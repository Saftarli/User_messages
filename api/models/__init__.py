from api.utils import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer,String,Text,Boolean,DateTime,ForeignKey
from datetime  import datetime as dt


class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    username: Mapped[str] = mapped_column(String(50),unique=True,nullable=False)
    email: Mapped[str] = mapped_column(String(45),nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(250),nullable=False)
    # contacts: Mapped["Contact"] = relationship('Contact',backref='owner',lazy=True)
    # messages_sent: Mapped["Message"]= relationship('Message', backref='sender',lazy=True)
    # messages_received: Mapped["Message"]= relationship('Message', backref='recipient',lazy=True)
    

    def __repr__(self):
        return f"<User {self.username}>"
    
    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)

class Contact(db.Model):
    __tablename__ = 'contacts'

    id: Mapped[int]= mapped_column(Integer,primary_key=True)
    owner_id: Mapped[int]= mapped_column(Integer,ForeignKey('users.id'), nullable=False)
    contact_id: Mapped[int]=mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    # contact_user: Mapped['User']=relationship('User',backref='added_contacts')

    def __repr__(self):
        return f"<Contact {self.id}>"
    
    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)
    
class Message(db.Model):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey('user_id', nullable= False))
    recipent_id: Mapped[int] = mapped_column(Integer, ForeignKey('user_id', nullable= False))
    datetime: Mapped[dt]= mapped_column(DateTime,default=dt.utcnow)
    content: Mapped[str] = mapped_column(Text,nullable=False)
    status: Mapped[str] = mapped_column(String(10), default='Send')


    def __repr__(self):
        return f"<Contact {self.id}>"
    
    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)



