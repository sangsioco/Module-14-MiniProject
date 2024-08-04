import graphene
from schema import Movie
from models.movie import Movie as MovieModel
from models.genre import Genre as GenreModel
from database import db
from sqlalchemy.orm import Session

class MovieQuery(graphene.ObjectType):
    movies = graphene.List(Movie)
    get_movies_by_genre = graphene.List(Movie, genre_id=graphene.Int(required=True))

    def resolve_movies(self, info):
        return db.session.execute(db.select(MovieModel)).scalars().all()

    def resolve_get_movies_by_genre(self, info, genre_id):
        with Session(db.engine) as session:
            result = session.execute(
                db.select(MovieModel).join(MovieModel.genres).where(GenreModel.id == genre_id)
            )
            return result.unique().scalars().all()
