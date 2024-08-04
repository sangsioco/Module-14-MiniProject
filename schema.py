import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models.movie import Movie as MovieModel
from models.genre import Genre as GenreModel


# Define the Genre GraphQL type
class Genre(SQLAlchemyObjectType):
    class Meta:
        model = GenreModel

# Define the Movie GraphQL type with genres field
class Movie(SQLAlchemyObjectType):
    class Meta:
        model = MovieModel
        interfaces = (graphene.relay.Node,)

    # Add a field for associated genres
    genres = graphene.List(Genre)

    def resolve_genres(self, info):
        return self.genres

