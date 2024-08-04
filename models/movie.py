from sqlalchemy.orm import Mapped, mapped_column
from database import db, Base
from typing import List


class Movie(Base):
    __tablename__ = 'movies'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(255))
    director: Mapped[str] = mapped_column(db.String(255))
    year: Mapped[int] = mapped_column(db.Integer)
    # relationship movie to genre
    genres: Mapped[List['Genre']] = db.relationship('Genre', secondary="movie_genre_association", back_populates='movies', lazy='joined')

