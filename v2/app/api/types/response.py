import graphene
from .error import FieldError
from ..user import User


class DeleteResponse(graphene.ObjectType):
    completed = graphene.Boolean(default_value=False)
    errors = graphene.List(FieldError, default_value=[])


class AuthResponse(graphene.ObjectType):
    user = graphene.Field(User, default_value=None)
    errors = graphene.List(FieldError, default_value=[])
    access_token = graphene.String(default_value='')
    refresh_token = graphene.String(default_value='')


class RefreshResponse(graphene.ObjectType):
    new_access_token = graphene.String()
    new_refresh_token = graphene.String()
