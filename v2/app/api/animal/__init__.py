import graphene
import app.api.user as User
import app.api.zoo as Zoo


class Animal(graphene.ObjectType):
    id = graphene.Int()
    owner_id = graphene.Int()
    owner = graphene.Field(User)
    zoo_id = graphene.Int(required=False)
    zoo = graphene.Field(Zoo, required=False)
