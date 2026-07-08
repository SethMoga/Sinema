from flask import Blueprint, request, jsonify, redirect, render_template
from services.user_service import create_user
from services.user_service import delete_user
from services.user_service import update_user
from services.media_service import *


from flask import session
from db import db
from models.user import User
from models.saved_media import SavedMedia
from models.review import Review
from pprint import pprint


user_bp = Blueprint("user", __name__)

@user_bp.route('/user/<name>')
def user(name):
    if "user_id" in session and db.session.get(User, session["user_id"]).username == name:
        print("Logged in as:", session["user_id"])
        user_data = db.session.get(User, session["user_id"])
        
        #################TEMPORARY#################
        user_saved_media = SavedMedia.query.filter_by(user_id=session["user_id"]).all()
        user_reviews = Review.query.filter_by(user_id=session["user_id"]).all()
        
        user_sm_data = []
        
        print(user_saved_media)
        
        for sm in user_saved_media:
            sm_dict = {}
            sm_dict["id"] = sm.id
            sm_dict["tmdb_id"] = sm.tmdb_id
            sm_dict["media_type"] = sm.media_type
            
            print("ID:", sm.id)
            print("tmdb id:", sm.tmdb_id)
            print("media type:", sm.media_type)
            
            if sm.media_type == "movie":
                #   pprint(temp_movie_info(sm.tmdb_id))
                sm_dict["card_data"] = temp_movie_info(sm.tmdb_id)
            else:
                #   pprint(temp_tv_show_info(sm.tmdb_id))
                sm_dict["card_data"] = temp_tv_show_info(sm.tmdb_id)
            
            user_sm_data.append(sm_dict)
            
            #   print()
        #################TEMPORARY#################
        pprint(user_sm_data)
        
        print(user_reviews)
        
        
        return render_template('user_profile.html', user_data=user_data, user_sm_data=user_sm_data, user_saved_media=user_saved_media, user_reviews=user_reviews)
    
    return redirect('/')


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    print('ON REGISTER ROUTE')

    if request.method == 'POST':
        #get data from form
        data = request.form
        print(data)

        #local vars
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
        
        print("email:", email)
        print("username:", username)
        print("password:", password)

        #call service functions
        result = create_user(email, username, password)
        
        if result:
            return redirect('/login')
    
    return render_template('register.html')

@user_bp.route('/delete-user', methods=['DELETE'])
def delete_user_route():

    data = request.form

    user_id = data.get("user_id")

    result = delete_user(user_id)
    
    return jsonify(result)

@user_bp.route('/update-user', methods=['POST'])
def update_user_route():

    data = request.form

    user_id = data.get("user_id")
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    result = update_user(user_id, email, username, password)

    return jsonify(result)
