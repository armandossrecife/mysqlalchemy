import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import bcrypt

Base = declarative_base()

# User model
class User(Base):
    """Model representing a user in the database."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(254), unique=True, nullable=False)
    password_hash = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now())
    
    # Cria um relacionamento com a classe Note
    notes = relationship("Note")

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())   

# Note model
class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True) 
    description = Column(String(1000))
    created_at = Column(DateTime, default=datetime.datetime.now())
    # Define a chave estrangeira (FK) para a tabela users
    user_id = Column(Integer, ForeignKey("users.id"))