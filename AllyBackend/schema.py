import graphene

from Website.schema.schema import Mutation, Query


class Query(Query, graphene.ObjectType):

    pass


class Mutation(Mutation, graphene.ObjectType):

    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
