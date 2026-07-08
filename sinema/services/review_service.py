from db import db
from models.review import Review

def create_review(user_id, tmdb_id, media_type, review_title, review_text, rating):
    
    #check if review exists
    existing_review = Review.query.filter_by(user_id=user_id, tmdb_id=tmdb_id, media_type=media_type).first()
    if existing_review:
        return False

    #create new review object
    new_review = Review(user_id=user_id, tmdb_id=tmdb_id, media_type=media_type, review_title=review_title, review_text=review_text, rating=rating)

    #add to db
    db.session.add(new_review)
    db.session.commit()

    return True

def delete_review(review_id):

    #check if review exists
    existing_review = Review.query.get(review_id)
    if not existing_review:
        return {"error ": "Review not found"}
    
    db.session.delete(existing_review)
    db.session.commit()

    return {"message": "Review successfully deleted"}

def update_review(review_id, review_text, review_rating):

    #check if review exists
    existing_review = Review.query.get(review_id)
    if not existing_review:
        return {"error ": "Review not found"}
    
    #set new values
    existing_review.review_text = review_text
    existing_review.review_rating = review_rating

    db.session.commit()

    return {"message": "Review updated successfully"}
    
