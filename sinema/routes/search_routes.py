from flask import Blueprint, request, render_template, redirect, jsonify
from services.search_service import search_tmdb
from db import db
from models.user import User
from flask import session

search_bp = Blueprint("search", __name__)

@search_bp.route('/search', methods=['GET'])
def search():

    user_data = {}
    
    if "user_id" in session:
        user_data = db.session.get(User, session["user_id"])
    
    #value of a query string parameter 'search' from the URL
    search = request.args.get('search')
    
    #if 'search' parameter from query string does not have a value (empty), redirect client to the home route
    if search is None:
        return redirect('/')
    
    #list of movie/tv-show results
    results = search_tmdb(search)
        
    return render_template("search.html", results=results, user_data=user_data)