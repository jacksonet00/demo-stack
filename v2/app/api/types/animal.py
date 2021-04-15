import graphene
from .error import FieldError
from ..animal import Animal


class AnimalInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    owner_id = graphene.Int(required=True)
    zoo_id = graphene.Int()


class AnimalResponse(graphene.ObjectType):
    animal = graphene.Field(Animal, default_value=None)
    errors = graphene.List(FieldError, default_value=[])
