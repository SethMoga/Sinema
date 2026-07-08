from db import db
from datetime import datetime

class SavedMedia(db.Model):
    __tablename__ = "saved_media"

    id = db.Column(db.Integer, primary_key=True)

    tmdb_id = db.Column(db.Integer, nullable=False, index=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    media_type = db.Column(db.Enum("movie", "tv", name="media_type_enum"), nullable=False)
    
    #prevent duplicates
    __table_args__ = (
        db.UniqueConstraint("user_id", "tmdb_id", "media_type", name="unique_user_media"),
    )

    #track when media was saved
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)

    #db relationship one to many with user
    user = db.relationship("User", back_populates="saved_media")

    '''
    #db relationship one to one with review
    review = db.relationship("Review", back_populates="saved_media", uselist=False, cascade="all, delete-orphan")
    '''
