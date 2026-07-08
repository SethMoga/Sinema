from flask import Blueprint, request, render_template, jsonify
from services.media_service import *
from models.user import User
from models.review import Review
from flask import session

media_bp = Blueprint("media", __name__)

@media_bp.route('/save-media', methods=['POST'])
def save_media_route():
    if "user_id" in session:
        print("ADD TO FAVORITES")
        data = request.get_json()
        print(data)
        
        tmdb_id = data.get("tmdb_id")
        media_type = data.get("media_type")

        #call service function
        result = save_media(session["user_id"], tmdb_id, media_type)
        
        #created a new resource STATUS CODE: 201 CREATED
        return {"message": "Created successfully"}, 201
    
    return {"message": "Logical fail"}, 409

@media_bp.route('/movies/<id>')
def movies(id):
    user_data = {}
    
    if "user_id" in session:
        user_data = db.session.get(User, session["user_id"])

    favorite_flag = False;
    
    #SQL query that JOINS Review table with User table
    reviews = db.session.query(Review, User).join(User, Review.user_id == User.id).filter(
        Review.tmdb_id == id,
        Review.media_type == "movie"
    ).all()
    
    
    print("All USERS FOR THIS REVIEW SECTION:")
    for review, user in reviews:
        print(user.username, "==>", review.review_text)
    
    if "user_id" in session:
        favorite_flag = saved_media_exist(session["user_id"], id, "movie")
    
    info = get_movie_info(id)
    
    print(f"Favorite flag: {favorite_flag}")
    
    return render_template("info.html", info=info, favorite_flag=favorite_flag, reviews=reviews, user_data=user_data,)


@media_bp.route('/tv-series/<id>')
def tv_series(id):
    user_data = {}
    
    if "user_id" in session:
        user_data = db.session.get(User, session["user_id"])

    favorite_flag = False;
    
    #SQL query that JOINS Review table with User table
    reviews = db.session.query(Review, User).join(User, Review.user_id == User.id).filter(
        Review.tmdb_id == id,
        Review.media_type == "tv"
    ).all()
    
    
    print("All USERS FOR THIS REVIEW SECTION:")
    for review, user in reviews:
        print(user.username, "==>", review.review_text)
    
    if "user_id" in session:
        favorite_flag = saved_media_exist(session["user_id"], id, "tv")
    
    info = get_tv_show_info(id)
    
    print(f"Favorite flag: {favorite_flag}")
    
    return render_template("info.html", info=info, favorite_flag=favorite_flag, reviews=reviews, user_data=user_data,)


@media_bp.route('/delete-media', methods=['DELETE'])
def delete_media_route():
    if "user_id" in session:
        print("REMOVE FROM FAVORITES")
        data = request.get_json()
        print(data)
        
        tmdb_id = data.get("tmdb_id")
        media_type = data.get("media_type")
        
        #call service function
        result = delete_media(session["user_id"], tmdb_id, media_type)
        
        #created a new resource STATUS CODE: 204 NO CONTENT
        return {"message": "Deleted successfully"}, 204

    return {"message": "Logical fail"}, 409    
    '''
    #get data from json
    data = request.get_json()

    #pull saved media id
    saved_media_id = data.get("saved_media_id")

    #call service function to delete
    result = delete_media(saved_media_id)

    return jsonify(result)
    '''


    