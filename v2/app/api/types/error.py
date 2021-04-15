import graphene


class FieldError(graphene.ObjectType):
    field = graphene.String()
    message = graphene.String()
