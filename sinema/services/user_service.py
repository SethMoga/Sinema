import requests
from models.user import User
from werkzeug.security import generate_password_hash
from db import db

def create_user(email, username, password):

    #check for input
    if not username or not password or not email:
        return {"error": "Username, password, and email are required"}
   
    #check for existing username
    existing_username = User.query.filter_by(username=username).first()
    if existing_username:
        print("error:", "Username already in use")
        return False
   
    #check for existing email
    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        print("error:", "Email already in use")
        return False
   
    #hash password
    #    hashed_password = generate_password_hash(password)

    #create new user object
    new_user = User(email=email, username=username, password_hash=password)
    new_user.set_password(new_user.password_hash)

    #commit to db
    db.session.add(new_user)
    db.session.commit()

    print("message:", "User created successfully")
    return True

def delete_user(user_id):
   
   #ensure proper id is passed
   if not user_id:
      return {"error": "User ID is required"}

   #query databse with id
   user = User.query.get(user_id)

   #validate user exists 
   if not user:
      return {"error": "User not found"}
   
   db.session.delete(user)
   db.session.commit()

   return {"error": "User deleted"}

def update_user(user_id, email=None, username=None, password=None):
   
   if not user_id:
      return {"error": "User ID required"}
   
   user = User.query.get(user_id)

   if not user:
      return {"error": "User not found"}
   
   #check to see if username is already used
   if username:
      existing_username = User.query.filter_by(username=username).first()
      if existing_username.id != user.user_id:
         return {"error": "Username already in use"}
      user.username = username

    #check to see if email is already used
   if email:
      existing_email = User.query.filter_by(email=email).first()
      if existing_email.id != user.user_id:
         return {"error ": "Email already in use"}
      user.email = email     

   if password:
      user.password_hash = generate_password_hash

   db.session.commit()

   return {"User updated sucessfully"}
   
