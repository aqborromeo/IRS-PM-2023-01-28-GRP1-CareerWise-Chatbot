from sqlalchemy import func
from dataclasses import dataclass
from sqlalchemy.orm import relationship

from app.models.occupation import Occupation
from app.models.chat_session import ChatSession

from app.db import db


@dataclass
class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True, index=True)
    occupation_id = db.Column(db.ForeignKey(Occupation.id))

    interest_similarity = db.Column(db.Float)
    experience_similarity = db.Column(db.Float)
    context_similarity = db.Column(db.Float)
    salary_similarity = db.Column(db.Float)
    score = db.Column(db.Float)

    user_rating = db.Column(db.Integer)

    chat_session_id = db.Column(db.ForeignKey(ChatSession.id))

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(), onupdate=func.now())

    chat_session = relationship("ChatSession", back_populates="results")
    occupation = relationship("Occupation")
