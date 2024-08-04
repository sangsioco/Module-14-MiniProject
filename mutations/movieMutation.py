import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models.movie import Movie as MovieModel
from models.genre import Genre as GenreModel
from database import db
from sqlalchemy.orm import Session
from schema import Movie

class AddMovie(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        director = graphene.String(required=True)
        year = graphene.Int(required=True)
        genre_ids = graphene.List(graphene.Int)

    movie = graphene.Field(Movie)

    def mutate(self, info, title, director, year, genre_ids=None):
        with Session(db.engine) as session:
            with session.begin():
                movie = MovieModel(title=title, director=director, year=year)
                session.add(movie)

                if genre_ids:
                    genres = session.execute(db.select(GenreModel).where(GenreModel.id.in_(genre_ids))).scalars().all()
                    movie.genres.extend(genres)

            session.refresh(movie)
            return AddMovie(movie=movie)

class UpdateMovie(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String(required=True)
        director = graphene.String(required=True)
        year = graphene.Int(required=True)
        genre_ids = graphene.List(graphene.Int)

    movie = graphene.Field(Movie)

    def mutate(self, info, id, title, director, year, genre_ids=None):
        with Session(db.engine) as session:
            with session.begin():
                movie = session.execute(db.select(MovieModel).where(MovieModel.id == id)).scalars().first()
                if movie:
                    movie.title = title
                    movie.director = director
                    movie.year = year

                    if genre_ids is not None:
                        genres = session.execute(
                            db.select(GenreModel).where(GenreModel.id.in_(genre_ids))
                        ).scalars().all()
                        movie.genres = genres

                session.refresh(movie)
                return UpdateMovie(movie=movie)

class DeleteMovie(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    movie = graphene.Field(Movie)

    def mutate(self, info, id):
        with Session(db.engine) as session:
            with session.begin():
                movie = session.execute(db.select(MovieModel).where(MovieModel.id == id)).scalars().first()
                if movie:
                    session.delete(movie)
                else:
                    return None
            session.refresh(movie)
            return DeleteMovie(movie=movie)

class MovieMutation(graphene.ObjectType):
    create_movie = AddMovie.Field()
    update_movie = UpdateMovie.Field()
    delete_movie = DeleteMovie.Field()