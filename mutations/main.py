import graphene
from mutations.movieMutation import MovieMutation
from mutations.genreMutation import GenreMutation

class Mutation(MovieMutation, GenreMutation, graphene.ObjectType):
    pass

