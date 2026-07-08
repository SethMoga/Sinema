from models.user import User
from werkzeug.security import check_password_hash
from flask import session

def login_auth(username, password):
    user = User.query.filter_by(username=username).first()
    
    print("In login AUTH, user.password_hash is", user.password_hash)
    print("In login AUTH, password is", password)

    if not user:
        return {"error": "User not found"}

    if not user.check_password(password):
        return {"error": "Invalid password"}
    
    session["user_id"] = user.id
    return {"message": "Login successful", "user_id": user.id}

def logout_auth():
    if "user_id" not in session:
        return {"error:" "No user is logged in"}
    #   session["user_id"] = None;
    #   session.pop("user_id", None)
    session.clear()
    return {"message": "Logout successful"}
