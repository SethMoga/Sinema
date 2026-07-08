from flask import Blueprint, request, jsonify, redirect
from services.review_service import create_review
from services.review_service import delete_review
from services.review_service import update_review
from flask import session


review_bp = Blueprint("review", __name__)

@review_bp.route('/create-review', methods=['POST'])
def create_review_route():
    #get data from json
    data = request.form
    tmdb_id = data.get('tmdb_id')
    media_type = data.get("media_type")
    
    if "user_id" in session:
        print(data)
        
        #create local vars
        review_title = data.get("review_title")
        review_text = data.get("review_text")
        rating = data.get("rating")

        #call service method
        result = create_review(session["user_id"], tmdb_id, media_type, review_title, review_text, rating)
        
        print(f"SUCCESS: Review created" if result else f"FAILED: Review made by user ID {session['user_id']} already exists." )
    
    if media_type == "movie":
        return redirect(f"/movies/{tmdb_id}#reviews-list")
    elif media_type == "tv":
        return redirect(f"/tv-series/{tmdb_id}#reviews-list")
    
    return redirect('/')

@review_bp.route('/delete-review', methods=['DELETE'])
def delete_review_route():

    data = request.get_json()

    review_id = data.get("review_id")

    result = delete_review(review_id)

    return jsonify(result)

@review_bp.route('/update-review', methods=['POST'])
def update_review_route():

    data = request.get_json()

    review_id = data.get("review_id")
    review_text = data.get("review_text")
    review_rating = data.get("review_rating")

    result = update_review(review_id, review_text, review_rating)

    return jsonify(result)