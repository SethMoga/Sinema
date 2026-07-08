from db import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(100), unique=True, nullable=False)
    
    username = db.Column(db.String(100), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), unique=False, nullable=False)
    
    #track when user created account
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    #defines relationship (like @OneToMany)
    saved_media = db.relationship("SavedMedia", back_populates="user", cascade="all, delete-orphan")
    
    #defines relationship (like @OneToMany)
    review = db.relationship("Review", back_populates="user", cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)