import graphene
import app.api.animal as Animal
import app.api.user as User


class Zoo(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    owner_id = graphene.Int()
    owner = graphene.Field(User)
    animals = graphene.List(Animal)
