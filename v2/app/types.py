import graphene


class FieldError(graphene.ObjectType):
    field = graphene.String()
    message = graphene.String()


class DeleteResponse(graphene.ObjectType):
    completed = graphene.Boolean(default_value=False)
    errors = graphene.List(FieldError, default_value=[])


class RefreshResponse(graphene.ObjectType):
    new_access_token = graphene.String()
    new_refresh_token = graphene.String()


class AnimalInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    zoo_id = graphene.Int()


class ZooInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    owner_id = graphene.Int(required=True)


class UserInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)
