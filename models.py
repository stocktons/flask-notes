"""Models for Notes app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User."""
    
    __tablename__ = "users"

    username = db.Column(db.String(20), 
                        primary_key=True, 
                        autoincrement=True) 
    password = db.Column(db.String(100), 
                        nullable=False) 
    email = db.Column(db.String(50), 
                      nullable=False, 
                      unique=True)
    first_name = db.Column(db.String(30), 
                           nullable=False)
    last_name = db.Column(db.String(30), 
                          nullable=False) 

    
    def serialize(self):
        """Serialize dictionary"""
        return {
                "id": self.id,
                "flavor": self.flavor,
                "size": self.size,   
                "rating": self.rating,
                "image": self.image,
        }
