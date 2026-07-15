import requests
from pprint import pprint
import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")

#constants
#url = "https://api.themoviedb.org/3/person/popular?language=en-US&page=1"
MOVIE_URL = "https://api.themoviedb.org/3/search/movie"
TV_URL = "https://api.themoviedb.org/3/search/tv"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_API_KEY}"
}

def search_tmdb(search):
    #empty list
    res = []
    
    #assembles the query string
    params = {
        "query": search,
        "include_adult" : "false",
        "language" : "en-US",
        "page" : "1"
    }
    
    temp_res = requests.get("https://api.themoviedb.org/3/search/multi", headers=headers, params=params)
    
    print("=======================MULTI====================")
    print(temp_res.json()["total_pages"])
    pprint(temp_res.json()["results"])

    for media in temp_res.json()["results"]:
        
        #append movies to list that have been released
        if media.get("release_date") and media.get("media_type") == "movie":
            res.append({"id": str(media["id"]), "title": media["original_title"], "image": "https://image.tmdb.org/t/p/original" + media["poster_path"] if media["poster_path"] else "https://placehold.co/250x380", "url" : f"/movies/{media['id']}", "media_type": media["media_type"], "rating": media["vote_average"]})
        
        #append tv shows to list that have been aired
        if media.get("first_air_date") and media.get("media_type") == "tv":
            res.append({"id": str(media["id"]), "title": media["original_name"], "image": "https://image.tmdb.org/t/p/original" + media["poster_path"] if media["poster_path"] else "https://placehold.co/250x380", "url" : f"/tv-series/{media['id']}", "media_type": media["media_type"], "rating": media["vote_average"]})


    '''
    #Response objects
    movie_res = requests.get(MOVIE_URL, headers=headers, params=params)
    tv_res = requests.get(TV_URL, headers=headers, params=params)
    
    #   print("======Movies=======")
    for movie in movie_res.json()["results"]:
        #   print("Id - " + str(movie["id"]) + ": " + movie["original_title"])
        
        #append movies to list that have been released
        if movie["release_date"]:
            res.append({"id": str(movie["id"]), "title": movie["original_title"], "image": "https://image.tmdb.org/t/p/original" + movie["poster_path"] if movie["poster_path"] else "https://placehold.co/250x380", "url" : f"/movies/{movie['id']}"})
    
    #   print("======TV Shows=======")
    for tv in tv_res.json()["results"]:
        #   print("Id - " + str(tv["id"]) + ": " + tv["original_name"])
        
        #append tv shows to list that have been aired
        if tv["first_air_date"]:
            res.append({"id": str(tv["id"]), "title": tv["original_name"], "image": "https://image.tmdb.org/t/p/original" + tv["poster_path"] if tv["poster_path"] else "https://placehold.co/250x380", "url" : f"/tv-series/{tv['id']}"})
    '''
    return res