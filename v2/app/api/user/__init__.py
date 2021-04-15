import graphene
import app.api.zoo as Zoo
import app.api.animal as Animal


class User(graphene.ObjectType):
    id = graphene.Int()
    username = graphene.String()
    zoos = graphene.List(Zoo)
    animals = graphene.List(Animal)
