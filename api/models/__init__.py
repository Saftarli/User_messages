from api.utils import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime  
from datetime import datetime as dt



class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password_hash: Mapped[str] = mapped_column(String)


    def __repr__(self):
        return f"<User {self.username }>"
    
    
    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)
    

class Contact(db.Model):
    __tablename__ = 'contacts'

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    contact_id: Mapped[int] = mapped_column(Integer,ForeignKey('users.id'))
    name: Mapped[str] = mapped_column(String(30), nullable=True)
    

    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)
    

    def __repr__(self):
        return f"<Contact {self.id}>"
    

    def vurma(self):
        return self.id * self.owner_id
        
    
    def yoxla(self,id):
        return    self.id > 1000
    


class Message(db.Model):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    recipient_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    content: Mapped[str] = mapped_column(String,nullable=False)
    timestamp: Mapped[dt] = mapped_column(DateTime, default=dt.utcnow)


    def __repr__(self):
        return f"<Message {self.id}>"
    


    
