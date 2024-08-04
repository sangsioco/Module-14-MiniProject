from sqlalchemy.orm import Mapped, mapped_column
from database import db, Base
from typing import List

class Genre(Base):
    __tablename__ = 'genres'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255))
    # relationship genre to movie
    movies: Mapped[List['Movie']] = db.relationship('Movie', secondary="movie_genre_association", back_populates='genres')

# association table for many-to-many relationship
class MovieGenreAssociation(Base):
    __tablename__ = 'movie_genre_association'
    movie_id: Mapped[int] = mapped_column(db.ForeignKey('movies.id'), primary_key=True)
    genre_id: Mapped[int] = mapped_column(db.ForeignKey('genres.id'), primary_key=True)
