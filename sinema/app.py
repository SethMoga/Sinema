from flask import Flask, request, render_template, redirect, jsonify
from flask_session import Session
import requests
import os
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

load_dotenv()

from db import db
from routes.search_routes import search_bp
from routes.media_routes import media_bp
from routes.auth_routes import auth_bp
from routes.review_routes import review_bp
from routes.user_routes import user_bp
from flask import session

app = Flask(__name__)

# ══════════════════════════════════════════
#  Config
# ══════════════════════════════════════════

# TMDB - used to hydrate AI-returned titles with posters/ratings
MOVIE_URL = "https://api.themoviedb.org/3/search/movie"
TV_URL = "https://api.themoviedb.org/3/search/tv"
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")

TMDB_HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_API_KEY}"
}

# OpenRouter - the AI brain
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_KEY}",
    "Content-Type": "application/json",
}

MODELS = [
    "google/gemini-3-flash-preview"

]

AI_TITLE_COUNT = 20

# ══════════════════════════════════════════
#  Helpers
# ══════════════════════════════════════════

def get_poster(item):
    if item.get("poster_path"):
        return "https://image.tmdb.org/t/p/w500" + item["poster_path"]
    return "https://placehold.co/250x380"


def get_year(date_str):
    return date_str[:4] if date_str and len(date_str) >= 4 else ""


def tmdb_lookup(title):
    """Search TMDB for a single title. Returns dict or None."""
    params = {
        "query": title,
        "include_adult": "false",
        "language": "en-US",
        "page": "1"
    }

    # Try movies first
    try:
        r = requests.get(MOVIE_URL, headers=TMDB_HEADERS, params=params, timeout=10)
        print(f"[TMDB] Movie search for '{title}': status={r.status_code}")
        if r.status_code != 200:
            print(f"[TMDB] Error response: {r.text}")
        movies = r.json().get("results", [])
        if movies:
            m = movies[0]
            return {
                "id": str(m["id"]),
                "type": "movie",
                "title": m.get("title") or m.get("original_title") or "Unknown",
                "image": get_poster(m),
                "year": get_year(m.get("release_date", "")),
                "rating": m.get("vote_average", 0),
                "overview": m.get("overview", ""),
                "tmdb_url": f"https://www.themoviedb.org/movie/{m['id']}",
            }
    except Exception as e:
        print(f"[TMDB] Movie lookup failed for '{title}': {e}")

    # Fall back to TV
    try:
        r = requests.get(TV_URL, headers=TMDB_HEADERS, params=params, timeout=10)
        print(f"[TMDB] TV search for '{title}': status={r.status_code}")
        if r.status_code != 200:
            print(f"[TMDB] Error response: {r.text}")
        shows = r.json().get("results", [])
        if shows:
            t = shows[0]
            return {
                "id": str(t["id"]),
                "type": "tv",
                "title": t.get("name") or t.get("original_name") or "Unknown",
                "image": get_poster(t),
                "year": get_year(t.get("first_air_date", "")),
                "rating": t.get("vote_average", 0),
                "overview": t.get("overview", ""),
                "tmdb_url": f"https://www.themoviedb.org/tv/{t['id']}",
            }
    except Exception as e:
        print(f"[TMDB] TV lookup failed for '{title}': {e}")

    return None


def ai_recommend(description, count=AI_TITLE_COUNT):
    """Ask OpenRouter for movie titles. Returns list of strings."""
    for model in MODELS:
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        f"List exactly {count} movie titles matching the user's description. "
                        "Use English titles only. "
                        "One per line, numbered like '1. Title'. No other text."
                    )
                },
                {"role": "user", "content": description}
            ],
            "max_tokens": 600,
            "temperature": 0.7,
        }
        try:
            res = requests.post(OPENROUTER_URL, headers=OPENROUTER_HEADERS,
                                json=payload, timeout=30)
            data = res.json()
            if data.get("choices"):
                print(f"[AI] Used: {model}")
                raw = data["choices"][0]["message"]["content"]
                titles = []
                for line in raw.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    # Strip leading "1. ", "2) ", etc.
                    for i, ch in enumerate(line):
                        if not ch.isdigit():
                            line = line[i:].lstrip(".):- ")
                            break
                    if line:
                        titles.append(line)
                return titles
        except Exception as e:
            print(f"[AI] {model} failed: {e}")
            continue

    return []



#implementation for session key
app.secret_key = "test"

#database config
#this is the database i want to connect to
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
#disable unneccessary tracking
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#attach database settings so it knows how to behave
db.init_app(app)

# ---------------- Configuration ----------------
app.config["SESSION_PERMANENT"] = False     # Sessions expire when browser closes
app.config["SESSION_TYPE"] = "filesystem"     # Store session data on the filesystem
app.config["SESSION_FILE_DIR"] = "/tmp/flask_session"
Session(app)

#import after initialization
from models.user import User
from models.saved_media import SavedMedia
from models.review import Review

#connect route to main
app.register_blueprint(search_bp)
app.register_blueprint(media_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(review_bp)
app.register_blueprint(user_bp)

@app.route('/')
def index():
    user_data = {}
    
    if "user_id" in session:
        user_data = db.session.get(User, session["user_id"])


    ######DISCLAIMER: THE FOLLOWING CODE IN THIS FUNCTION MAY BE LATER MODIFIED/MOVED TO DIFFERENT SCRIPT(S)############
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_KEY}"
    }
    # get latest released movies from TMDB (now playing)
    params = {
        "language": "en-US",
        "page": 1
    }
    try:
        now_playing_res = requests.get("https://api.themoviedb.org/3/movie/now_playing", headers=headers, params=params)
        now_playing_res.raise_for_status()
        now_playing_data = now_playing_res.json().get("results", [])
    except Exception:
        now_playing_data = []

    carousel_movies = []
    for movie in now_playing_data[:8]:
        poster_path = movie.get("poster_path")
        movie_id = movie.get("id")
        carousel_movies.append({
            "id": movie_id,
            "title": movie.get("title") or movie.get("name") or "Untitled",
            "release_date": movie.get("release_date", "Unknown"),
            "overview": movie.get("overview", "No description available."),
            "poster_url": f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://placehold.co/300x450?text=No+Image",
            "tmdb_url": f"https://www.themoviedb.org/movie/{movie_id}" if movie_id else "#"
        })
        
    #load the 'index.html' page to client (browser)
    return render_template("index.html", user_data=user_data, carousel_movies=carousel_movies)


@app.route('/home')
def home():
    return redirect('/')

@app.route('/movies')
def movies():
    user_data = {}
    
    if "user_id" in session:
        user_data = db.session.get(User, session["user_id"])
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_KEY}"
    }
    params = {
        "language": "en-US",
        "page": 1
    }
    try:
        movies_res = requests.get("https://api.themoviedb.org/3/movie/now_playing", headers=headers, params=params)
        movies_res.raise_for_status()
        movies_data = movies_res.json().get("results", [])
    except Exception:
        movies_data = []

    movies_list = []
    for movie in movies_data:
        poster_path = movie.get("poster_path")
        movie_id = movie.get("id")
        movies_list.append({
            "id": movie_id,
            "title": movie.get("title") or "Untitled",
            "release_date": movie.get("release_date", "Unknown"),
            "overview": movie.get("overview", "No description available."),
            "poster_url": f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://placehold.co/300x450?text=No+Image",
            "tmdb_url": f"https://www.themoviedb.org/movie/{movie_id}" if movie_id else "#"
        })

    return render_template("movies.html", user_data=user_data, movies=movies_list, page_title="Recent Movies")

@app.route('/tv')
def tv():
    user_data = {}
    
    if "user_id" in session:
        user_data = db.session.get(User, session["user_id"])

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_KEY}"
    }
    params = {
        "language": "en-US",
        "page": 1
    }
    try:
        tv_res = requests.get("https://api.themoviedb.org/3/tv/on_the_air", headers=headers, params=params)
        tv_res.raise_for_status()
        tv_data = tv_res.json().get("results", [])
    except Exception:
        tv_data = []

    tv_list = []
    for show in tv_data:
        poster_path = show.get("poster_path")
        show_id = show.get("id")
        tv_list.append({
            "id": show_id,
            "title": show.get("name") or "Untitled",
            "release_date": show.get("first_air_date", "Unknown"),
            "overview": show.get("overview", "No description available."),
            "poster_url": f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://placehold.co/300x450?text=No+Image",
            "tmdb_url": f"https://www.themoviedb.org/tv/{show_id}" if show_id else "#"
        })

    return render_template("tv.html", user_data=user_data, tv_shows=tv_list, page_title="Recent TV Shows")

@app.route('/trending')
def trending():
    user_data = {}
    
    if "user_id" in session:
        user_data = db.session.get(User, session["user_id"])
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_KEY}"
    }
    try:
        trending_res = requests.get("https://api.themoviedb.org/3/trending/movie/day", headers=headers)
        trending_res.raise_for_status()
        trending_data = trending_res.json().get("results", [])
    except Exception:
        trending_data = []

    trending_list = []
    for movie in trending_data:
        poster_path = movie.get("poster_path")
        movie_id = movie.get("id")
        trending_list.append({
            "id": movie_id,
            "title": movie.get("title") or movie.get("name") or "Untitled",
            "release_date": movie.get("release_date", "Unknown"),
            "overview": movie.get("overview", "No description available."),
            "poster_url": f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://placehold.co/300x450?text=No+Image",
            "tmdb_url": f"https://www.themoviedb.org/movie/{movie_id}" if movie_id else "#"
        })

    return render_template("trending.html", user_data=user_data, trending_movies=trending_list, page_title="Trending Movies")


@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/forgot-password', methods=['POST'])
def forgot_password_post():
    # TODO: Add password reset logic here
    return redirect('/')


@app.route('/ai_search')
def ai_search():
    user_data = {}
    
    if "user_id" in session:
        user_data = db.session.get(User, session["user_id"])

    return render_template('ai_search.html', user_data=user_data)

# ══════════════════════════════════════════
#  AI Search API Endpoint
# ══════════════════════════════════════════

@app.route('/api/ai-search', methods=['GET'])
def api_ai_search():
    """
    AI-powered movie recommendations.
    GET /api/ai-search?search=war+movies   
    """
    query = request.args.get('search', '').strip()
    if not query:
        return jsonify({"error": "Missing 'search' parameter"}), 400

    # Step 1: ask AI for titles
    titles = ai_recommend(query)
    if not titles:
        return jsonify({
            "error": "AI search failed. Check OPENROUTER_API_KEY.",
            "query": query,
            "results": [],
        }), 500

    print(f"[AI] Got titles: {titles}")

    # Step 2: parallel TMDB lookups to get posters/ratings
    with ThreadPoolExecutor(max_workers=20) as executor:
        matches = list(executor.map(tmdb_lookup, titles))

    print(f"[TMDB] Got matches: {matches}")

    # Step 3: dedupe by id, drop None
    seen = set()
    results = []
    for m in matches:
        if m and m["id"] not in seen:
            seen.add(m["id"])
            results.append(m)

    return jsonify({
        "query": query,
        "count": len(results),
        "results": results,
    })

if __name__ == '__main__':
    #create db file -TEMP- ===UNCOMMENT THIS TO CREATE LOCAL DB FILE===
    with app.app_context():
        db.create_all()
        
        '''
        #create test user for op checks 
        test_user = User(email="abc@gmail.com", username="abc", password_hash="1234")
        test_user.set_password(test_user.password_hash)
        db.session.add(test_user)
        db.session.commit()

        #create SavedMedia records for user id '3' (username: abc)
        test_sm1 = SavedMedia(tmdb_id=447273, user_id=3, media_type="movie")
        db.session.add(test_sm1)
        db.session.commit()
        
        test_sm2 = SavedMedia(tmdb_id=1396, user_id=3, media_type="tv")
        db.session.add(test_sm2)
        db.session.commit()
        
        test_r1 = Review(tmdb_id=1996, user_id=3, media_type="tv", review_title="One of the Best Shows in Cartoon History", review_text="The Flintstones is handsdown one of the best and iconic classic cartoons. I wish modern cartoons would follow this formula.", rating=4.5)
        db.session.add(test_r1)
        db.session.commit()
        '''
        
        '''
        #create test user for op checks 
        test_user = User(email="alphadude832@gmail.com", username="The Alpha Dude", password_hash="pizza9")
        test_user.set_password(test_user.password_hash)
        db.session.add(test_user)
        db.session.commit()
        '''
        
    app.run()
