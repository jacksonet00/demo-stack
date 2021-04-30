import graphene
from .engine import db_session
from .model import (User as UserModel, Zoo as ZooModel)
from .util import (user_loader, zoo_loader)


class Animal(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    owner_id = graphene.Int()
    owner = graphene.Field(lambda: User)
    zoo_id = graphene.Int(required=False)
    zoo = graphene.Field(lambda: Zoo, required=False)
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()

    @ staticmethod
    def resolve_owner(parent, info):
        return user_loader.load(parent.owner_id)

    @ staticmethod
    def resolve_zoo(parent, info):
        return zoo_loader.load(parent.zoo_id)


class Zoo(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    owner_id = graphene.Int()
    owner = graphene.Field(lambda: User)
    animals = graphene.List(Animal)
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()

    @ staticmethod
    def resolve_owner(parent, info):
        return user_loader.load(parent.owner_id)


class User(graphene.ObjectType):
    id = graphene.Int()
    username = graphene.String()
    zoos = graphene.List(Zoo)
    animals = graphene.List(Animal)
    profile_photo = graphene.String(required=False)
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()


class PaginatedAnimals(graphene.ObjectType):
    animals = graphene.List(Animal)
    has_more = graphene.Boolean()


class PaginatedZoos(graphene.ObjectType):
    zoos = graphene.List(Zoo)
    has_more = graphene.Boolean()


class FieldError(graphene.ObjectType):
    field = graphene.String()
    message = graphene.String()


class AnimalInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    zoo_id = graphene.Int()


class ZooInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    owner_id = graphene.Int(required=True)


class UserInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)


class DeleteResponse(graphene.ObjectType):
    completed = graphene.Boolean(default_value=False)
    errors = graphene.List(FieldError, default_value=[])


class RefreshResponse(graphene.ObjectType):
    new_access_token = graphene.String()
    new_refresh_token = graphene.String()


class AnimalResponse(graphene.ObjectType):
    animal = graphene.Field(Animal, default_value=None)
    errors = graphene.List(FieldError, default_value=[])


class ZooResponse(graphene.ObjectType):
    zoo = graphene.Field(Zoo, default_value=None)
    errors = graphene.List(FieldError, default_value=[])


class UserResponse(graphene.ObjectType):
    user = graphene.Field(User, default_value=None)
    errors = graphene.List(FieldError, default_value=[])


class AuthResponse(graphene.ObjectType):
    user = graphene.Field(User, default_value=None)
    errors = graphene.List(FieldError, default_value=[])
    access_token = graphene.String(default_value='')
    refresh_token = graphene.String(default_value='')
