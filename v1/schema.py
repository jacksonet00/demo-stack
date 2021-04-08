import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Animal as AnimalModel

# GraphQL Model
class Animal(SQLAlchemyObjectType):
    class Meta:
        model = AnimalModel
        interfaces = (relay.Node, )

# Queries
class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_animals = SQLAlchemyConnectionField(Animal.connection)

# Mutations
class CreateAnimal(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String(required=True)

    class Arguments:
        name = graphene.String()

    def mutate(self, info, name):
        animal = AnimalModel(name=name)
        db_session.add(animal)
        db_session.commit()

        return CreateAnimal(
            id=animal.id,
            name=animal.name
        )

class Mutation(graphene.ObjectType):
    create_animal = CreateAnimal.Field()

# GraphQL Schema
schema = graphene.Schema(query=Query, mutation=Mutation)
