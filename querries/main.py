import graphene
from querries.genreQuery import GenreQuery
from querries.movieQuery import MovieQuery

class Query(GenreQuery, MovieQuery, graphene.ObjectType):
    pass


