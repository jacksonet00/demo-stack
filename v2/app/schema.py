from passlib.hash import pbkdf2_sha256
from flask_graphql_auth import (
    AuthInfoField,
    GraphQLAuth,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    query_header_jwt_required,
    mutation_jwt_refresh_token_required,
    mutation_jwt_required,
    mutation_header_jwt_required
)
from .model import db_session, Animal as AnimalModel, User as UserModel
import graphene


class User(graphene.ObjectType):
    id = graphene.Int()
    username = graphene.String()
    password = graphene.String()


class InputError(graphene.ObjectType):
    field = graphene.String()
    message = graphene.String()


class UserInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)


class AuthOutput(graphene.ObjectType):
    user = graphene.Field(User, default_value=None)
    errors = graphene.List(InputError, default_value=[])
    access_token = graphene.String(default_value='')
    refresh_token = graphene.String(default_value='')


class Register(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    Output = AuthOutput

    @staticmethod
    def mutate(root, info, input):
        output = AuthOutput()
        errors = []
        user = db_session.query(UserModel).filter(
            UserModel.username == input.username).first()
        if user:
            errors.append(InputError(
                field='username', message='already taken'))
        if len(input.username) < 3:
            errors.append(InputError(field='username',
                                     message='must be at least 3 characters'))
        if len(input.password) < 3:
            errors.append(InputError(field='password',
                                     message='must be at least 3 characters'))
        output.errors = errors
        if not errors:
            hashed_password = pbkdf2_sha256.hash(input.password)
            new_user = UserModel(username=input.username,
                                 password=hashed_password)
            db_session.add(new_user)
            db_session.commit()
            output.user = new_user
            output.access_token = create_access_token(input.username)
            output.refresh_token = create_refresh_token(input.username)
        return output


class Login(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    Output = AuthOutput

    @staticmethod
    def mutate(root, info, input):
        output = AuthOutput()
        errors = []
        user = db_session.query(UserModel).filter(
            UserModel.username == input.username).first()
        if not user:
            errors.append(InputError(field='username',
                                     message='does not exist'))
        if user and not pbkdf2_sha256.verify(input.password, user.password):
            errors.append(InputError(field='password', message='incorrect'))
        output.errors = errors
        if not errors:
            output.user = user
            output.access_token = create_access_token(input.username)
            output.refresh_token = create_refresh_token(input.username)
        return output


class RefreshMutation(graphene.Mutation):
    class Arguments:
        refresh_token = graphene.String()

    new_access_token = graphene.String()
    new_refresh_token = graphene.String()

    @mutation_jwt_refresh_token_required
    def mutate(self):
        current_user = get_jwt_identity()
        return RefreshMutation(
            new_access_token=create_access_token(identity=current_user),
            new_refresh_token=create_refresh_token(identity=current_user)
        )


class Animal(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    computed_name = graphene.String()

    @staticmethod
    def resolve_computed_name(parent, info):
        return f'{parent.name}-007'


class AnimalInput(graphene.InputObjectType):
    name = graphene.String(required=True)


class AnimalOutput(graphene.ObjectType):
    animal = graphene.Field(Animal, default_value=None)
    errors = graphene.List(InputError, default_value=[])


class DeleteOutput(graphene.ObjectType):
    completed = graphene.Boolean(default_value=False)
    errors = graphene.List(InputError, default_value=[])


class CreateAnimal(graphene.Mutation):
    class Arguments:
        input = AnimalInput(required=True)

    Output = AnimalOutput

    @staticmethod
    @mutation_header_jwt_required
    def mutate(root, info, input=None):
        output = AnimalOutput()
        errors = []
        if len(input.name) < 3:
            errors.append(InputError(
                field='name', message='must be at least 3 characters'))
        output.errors = errors
        if not errors:
            animal = AnimalModel(name=input.name)
            db_session.add(animal)
            db_session.commit()
            output.animal = animal
        return output


class UpdateAnimal(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        name = graphene.String()

    Output = AnimalOutput

    @staticmethod
    @mutation_header_jwt_required
    def mutate(root, info, id=None, name=None):
        output = AnimalOutput()
        errors = []
        animal = db_session.query(
            AnimalModel).filter(AnimalModel.id == id).one()
        if not animal:
            errors.append(InputError(field='id', message='not found'))
        if len(name) < 3:
            errors.append(InputError(
                field='name', message='must be at least 3 characters'))
        output.errors = errors
        if not errors:
            animal.name = name
            db_session.commit()
            output.animal = animal
        return output


class DeleteAnimal(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    Output = DeleteOutput

    @staticmethod
    @mutation_header_jwt_required
    def mutate(root, info, id):
        output = DeleteOutput()
        animal = db_session.query(
            AnimalModel).filter(AnimalModel.id == id).one()
        if not animal:
            output.errors.append(InputError(field='id', message='not found'))
        if not output.errors:
            try:
                db_session.delete(animal)
                db_session.commit()
                output.completed = True
            except:
                pass
        return output


class Query(graphene.ObjectType):
    animal = graphene.Field(Animal, id=graphene.Int(required=True))

    @staticmethod
    def resolve_animal(parent, info, id):
        return db_session.query(AnimalModel).filter(AnimalModel.id == id).one()

    all_animals = graphene.List(Animal)

    @staticmethod
    def resolve_all_animals(parent, info):
        return db_session.query(AnimalModel).all()

    all_users = graphene.Field(User)

    @staticmethod
    def resolve_all_users(parent, info):
        return db_session.query(UserModel).all()


class Mutation(graphene.ObjectType):
    create_animal = CreateAnimal.Field()
    update_animal = UpdateAnimal.Field()
    delete_animal = DeleteAnimal.Field()

    login = Login.Field()
    register = Register.Field()
    refresh = RefreshMutation.Field()


Schema = graphene.Schema(query=Query, mutation=Mutation)
