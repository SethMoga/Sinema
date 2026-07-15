from db import db
from models.user import User
from models.saved_media import SavedMedia
import requests
from pprint import pprint
import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_API_KEY}"
}

#assembles the query string
params = {
    "language" : "en-US",
    "adult" : "false"
}

def saved_media_exist(user_id, tmdb_id, media_type):
    #check if media already saved
    existing = SavedMedia.query.filter_by(user_id=user_id, tmdb_id=tmdb_id, media_type=media_type).first()
    
    if existing:
        return True
    
    return False

def get_movie_info(id):
    #Response object
    movie_res = requests.get(f"https://api.themoviedb.org/3/movie/{id}", headers=headers, params=params)
    movie_vid_res = requests.get(f"https://api.themoviedb.org/3/movie/{id}/videos", headers=headers, params=params)
    
    #dictionary
    data = movie_res.json()
    video_data = movie_vid_res.json()["results"]
    pprint(video_data)
    
    video_data2 = []
    
    for vd in video_data:
        if vd["site"] == "YouTube":
            video_data2.append(vd)
    
    #concatenates the full image url path if the value for the property "poster_path" is not empty. Otherwise, set to empty string
    poster_img_url = "https://image.tmdb.org/t/p/original" + data["poster_path"] if data["poster_path"] else "https://placehold.co/250x380"
    
    #XM
    release_date = data.get("release_date") or ""
    year_released = release_date.split("-")[0] if release_date else "N/A"

    runtime_minutes = data.get("runtime")
    runtime_display = f"{runtime_minutes} min" if runtime_minutes else "N/A"

    rating_value = data.get("vote_average")
    rating_display = f"{rating_value:.2f}" if rating_value is not None else "N/A"
    description = data.get("overview") or "No description available."
    
    info = {
        "id": data["id"],
        "title": data["original_title"],
        "image_url": poster_img_url,
        # show type, year released, rating, runtime, desc
        "show_type" : "Movie",
        "year_released" : year_released,
        "rating" : rating_display,
        "runtime" : runtime_display,
        "description": description,
        "videos": video_data2
    }
    
    return info


def get_tv_show_info(id): 
    #Response object
    tv_series_res = requests.get(f"https://api.themoviedb.org/3/tv/{id}", headers=headers, params=params)
    tv_vid_res = requests.get(f"https://api.themoviedb.org/3/tv/{id}/videos", headers=headers, params=params)
    
    #dictionary
    data = tv_series_res.json()
    video_data = tv_vid_res.json()["results"]
    pprint(video_data)
    
    video_data2 = []
    
    for vd in video_data:
        if vd["site"] == "YouTube":
            video_data2.append(vd)
    
    #concatenates the full image url path if the value for the property "poster_path" is not empty. Otherwise, set to empty string
    poster_img_url = "https://image.tmdb.org/t/p/original" + data["poster_path"] if data["poster_path"] else "https://placehold.co/250x380"
    
    #XM
    first_air_date = data.get("first_air_date") or ""
    year_released = first_air_date.split("-")[0] if first_air_date else "N/A"

    # TMDB TV runtime "episode_run_time" XM
    episode_times = data.get("episode_run_time") or []
    runtime_display = f"{episode_times[0]} min/episode" if episode_times else "N/A"
    rating_value = data.get("vote_average")
    rating_display = f"{rating_value:.2f}" if rating_value is not None else "N/A"
    description = data.get("overview") or "No description available."
    
    info = {
        "id": data["id"],
        "title": data["original_name"],
        "image_url": poster_img_url,
        #show type, year rel, rating, runtime, XM, desc
        "show_type": "TV Series",
        "year_released": year_released,
        "rating": rating_display,
        "runtime": runtime_display,
        "description": description,
        "videos": video_data2
    }
    
    return info


def save_media(user_id, tmdb_id, media_type):

    #check if user exists
    user = db.session.get(User, user_id)
    #user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}

    #check if media already saved
    existing = SavedMedia.query.filter_by(user_id=user_id, tmdb_id=tmdb_id, media_type=media_type).first()

    if existing:
        return {"message": "Media already saved"}

    #create new saved media
    new_media = SavedMedia(user_id=user_id, tmdb_id=tmdb_id, media_type=media_type)

    db.session.add(new_media)
    db.session.commit()

    return {"message": "Media saved successfully"}

def delete_media(user_id, tmdb_id, media_type):

    #check if user exists
    user = db.session.get(User, user_id)
    #user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}

    #query based on passed media id and check if it exists
    existing_media = SavedMedia.query.filter_by(user_id=user_id, tmdb_id=tmdb_id, media_type=media_type).first()
    
    if not existing_media:
        return {"error": "Media is not saved"}
    
    db.session.delete(existing_media)
    db.session.commit()

    return {"message": "Media deleted successfully"}



def temp_movie_info(id):
    #Response object
    movie_res = requests.get(f"https://api.themoviedb.org/3/movie/{id}", headers=headers, params=params)
    
    #dictionary
    data = movie_res.json()
    
    #concatenates the full image url path if the value for the property "poster_path" is not empty. Otherwise, set to empty string
    poster_img_url = "https://image.tmdb.org/t/p/original" + data["poster_path"] if data["poster_path"] else "https://placehold.co/250x380"
    
    info = {
        "title": data["original_title"],
        "image_url": poster_img_url,
        "url" : f"/movies/{id}"
    }
    
    return info


def temp_tv_show_info(id): 
    #Response object
    tv_series_res = requests.get(f"https://api.themoviedb.org/3/tv/{id}", headers=headers, params=params)
    
    #dictionary
    data = tv_series_res.json()
    
    #concatenates the full image url path if the value for the property "poster_path" is not empty. Otherwise, set to empty string
    poster_img_url = "https://image.tmdb.org/t/p/original" + data["poster_path"] if data["poster_path"] else "https://placehold.co/250x380"
    
    info = {
        "title": data["original_name"],
        "image_url": poster_img_url,
        "url" : f"/tv-series/{id}"
    }
    
    return info