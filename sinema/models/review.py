from db import db
from datetime import datetime

class Review(db.Model):
    __tablename__ = "review"

    id = db.Column(db.Integer, primary_key=True)
    
    tmdb_id = db.Column(db.Integer, nullable=False, index=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    media_type = db.Column(db.Enum("movie", "tv", name="media_type_enum"), nullable=False)
    
    #prevent duplicates
    __table_args__ = (
        db.UniqueConstraint("user_id", "tmdb_id", "media_type", name="unique_user_review"),
    )

    #   saved_media_id = db.Column(db.Integer, db.ForeignKey("saved_media.id"), unique=True, nullable=False)
    
    review_title = db.Column(db.Text, nullable=False)
    
    review_text = db.Column(db.Text, nullable=False)

    rating = db.Column(db.Float, nullable=False)
    
    #track when user created account
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    #db relationship one to many with user
    user = db.relationship("User", back_populates="review")
    
    '''
    #defines relationship one to one for saved media
    saved_media = db.relationship("SavedMedia", back_populates="review")
    '''