import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models.movie import Movie as MovieModel
from models.genre import Genre as GenreModel
from database import db
from sqlalchemy.orm import Session
from schema import Genre


class AddGenre(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    genre = graphene.Field(Genre)

    def mutate(self, info, name):
        if not name or len(name) > 255:
            raise Exception("Genre name must be between 1 and 255 characters.")
        
        with Session(db.engine) as session:
            with session.begin():
                genre = GenreModel(name=name)
                session.add(genre)
            session.refresh(genre)
            return AddGenre(genre=genre)

class UpdateGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)

    genre = graphene.Field(Genre)

    def mutate(self, info, id, name):
        if not name or len(name) > 255:
            raise Exception("Genre name must be between 1 and 255 characters.")
        
        with Session(db.engine) as session:
            with session.begin():
                genre = session.execute(db.select(GenreModel).where(GenreModel.id == id)).scalars().first()
                if genre:
                    genre.name = name
                else:
                    return None
            session.refresh(genre)
            return UpdateGenre(genre=genre)

class DeleteGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    genre = graphene.Field(Genre)

    def mutate(self, info, id):
        with Session(db.engine) as session:
            with session.begin():
                genre = session.execute(db.select(GenreModel).where(GenreModel.id == id)).scalars().first()
                if not genre:
                    raise Exception("Genre ID does not exist.")
                session.delete(genre)
            session.refresh(genre)
            return DeleteGenre(genre=genre)

class GenreMutation(graphene.ObjectType):
    create_genre = AddGenre.Field()
    update_genre = UpdateGenre.Field()
    delete_genre = DeleteGenre.Field()
