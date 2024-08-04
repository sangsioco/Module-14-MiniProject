import graphene
from schema import Genre
from models.genre import Genre as GenreModel
from models.movie import Movie as MovieModel
from database import db
from sqlalchemy.orm import Session

class GenreQuery(graphene.ObjectType):
    genres = graphene.List(Genre)
    get_genre_by_movie = graphene.List(Genre, movie_id=graphene.Int(required=True))
    
    def resolve_genres(self, info):
        return db.session.execute(db.select(GenreModel)).scalars().all()

    def resolve_get_genre_by_movie(self, info, movie_id):
        with Session(db.engine) as session:
            movie = session.execute(
                db.select(MovieModel).where(MovieModel.id == movie_id)
            ).scalars().first()

            if movie:
                return movie.genres
            return []
