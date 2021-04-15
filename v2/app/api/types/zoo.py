import graphene
import app.api.zoo as Zoo
from .error import FieldError


class ZooInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    owner_id = graphene.Int(required=True)


class ZooResponse(graphene.ObjectType):
    zoo = graphene.Field(Zoo, default_value=None)
    errors = graphene.List(FieldError, default_value=[])
