import graphene
from .types import FieldError, UserInput, RefreshResponse, AnimalInput, ZooInput, DeleteResponse
from flask_graphql_auth import mutation_header_jwt_refresh_token_required, mutation_header_jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from passlib.hash import pbkdf2_sha256
from .engine import db_session
from .model import Animal as AnimalModel, Zoo as ZooModel, User as UserModel
from promise import Promise
from promise.dataloader import DataLoader


def handle_animal_authorization_error(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            return AnimalResponse(errors=[FieldError(field='Authorization Header', message='invalid token')])
    return inner_function


def handle_zoo_authorization_error(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            return ZooResponse(errors=[FieldError(field='Authorization Header', message='invalid token')])
    return inner_function


def handle_user_authorization_error(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            return AuthResponse(errors=[FieldError(field='Authorization Header', message='invalid token')])
    return inner_function


class Animal(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    owner_id = graphene.Int()
    owner = graphene.Field(lambda: User)
    zoo_id = graphene.Int(required=False)
    zoo = graphene.Field(lambda: Zoo, required=False)
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()

    @staticmethod
    def resolve_owner(parent, info):
        return db_session.query(UserModel).filter(UserModel.id == parent.owner_id).first()

    @staticmethod
    def resolve_zoo(parent, info):
        return db_session.query(ZooModel).filter(ZooModel.id == parent.zoo_id).first()


class AnimalResponse(graphene.ObjectType):
    animal = graphene.Field(Animal, default_value=None)
    errors = graphene.List(FieldError, default_value=[])


class Zoo(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    owner_id = graphene.Int()
    owner = graphene.Field(lambda: User)
    animals = graphene.List(Animal)
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()

    @staticmethod
    def resolve_owner(parent, info):
        return db_session.query(UserModel).filter(UserModel.id == parent.owner_id).first()


class ZooResponse(graphene.ObjectType):
    zoo = graphene.Field(Zoo, default_value=None)
    errors = graphene.List(FieldError, default_value=[])


class User(graphene.ObjectType):
    id = graphene.Int()
    username = graphene.String()
    zoos = graphene.List(Zoo)
    animals = graphene.List(Animal)
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()


class AuthResponse(graphene.ObjectType):
    user = graphene.Field(User, default_value=None)
    errors = graphene.List(FieldError, default_value=[])
    access_token = graphene.String(default_value='')
    refresh_token = graphene.String(default_value='')


class CreateAnimal(graphene.Mutation):
    class Arguments:
        input = AnimalInput(required=True)

    Output = AnimalResponse

    @staticmethod
    @handle_animal_authorization_error
    @mutation_header_jwt_required
    def mutate(root, info, input):
        res = AnimalResponse()
        owner = db_session.query(UserModel).filter(
            UserModel.id == input.owner_id).first()
        if not owner:
            res.errors.append(FieldError(
                field='owner_id', message='user does not exist'))
        if input.zoo_id:
            zoo = db_session.query(ZooModel).filter(
                ZooModel.id == input.zoo_id)
            if not zoo:
                res.errors.append(FieldError(
                    field='zoo_id', message='zoo does not exist'))
        if not res.errors:
            animal = AnimalModel(name=input.name, owner_id=input.owner_id)
            if input.zoo_id:
                animal.zoo_id = input.zoo_id
            db_session.add(animal)
            db_session.commit()
            res.animal = animal
        return res


class UpdateAnimal(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()

    Output = AnimalResponse

    @staticmethod
    @handle_animal_authorization_error
    @mutation_header_jwt_required
    def mutate(root, info, id, name=None):
        res = AnimalResponse()
        animal = db_session.query(AnimalModel).filter(
            AnimalModel.id == id).first()
        if not animal:
            res.errors.append(FieldError(
                field='id', message='animal does not exist'))
        if not res.errors and animal.name != name:
            animal.name = name
            db_session.commit()
            res.animal = animal
        return res


class DeleteAnimal(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    Output = DeleteResponse

    @ staticmethod
    @handle_animal_authorization_error
    @ mutation_header_jwt_required
    def mutate(root, info, id):
        res = DeleteResponse()
        animal = db_session.query(AnimalModel).filter(
            AnimalModel.id == id).first()
        if not animal:
            res.errors.append(FieldError(
                field='id', message='animal does not exist'))
        if not res.errors:
            try:
                db_session.delete(animal)
                db_session.commit()
                res.completed = True
            except:
                pass
        return res


class MoveAnimal(graphene.Mutation):
    class Arguments:
        animal_id = graphene.Int(required=True)
        zoo_id = graphene.Int(required=True)

    Output = AnimalResponse

    @staticmethod
    @handle_animal_authorization_error
    @mutation_header_jwt_required
    def mutate(root, info, animal_id, zoo_id):
        res = AnimalResponse()
        animal = db_session.query(AnimalModel).filter(
            AnimalModel.id == animal_id).first()
        zoo = db_session.query(ZooModel).filter(ZooModel.id == zoo_id).first()
        if not animal:
            res.errors.append(FieldError(field='animal_id',
                              message='animal does not exist'))
        if not zoo:
            res.errors.append(FieldError(field='zoo_id',
                              message='zoo does not exist'))
        if not res.errors:
            animal.zoo_id = zoo_id
            db_session.commit()
            res.animal = animal
        return res


class TransferAnimal(graphene.Mutation):
    class Arguments:
        animal_id = graphene.Int(required=True)
        user_id = graphene.Int(required=True)

    Output = AnimalResponse

    @staticmethod
    @handle_animal_authorization_error
    @mutation_header_jwt_required
    def mutate(root, info, animal_id, user_id):
        res = AnimalResponse()
        animal = db_session.query(AnimalModel).filter(
            AnimalModel.id == animal_id).first()
        user = db_session.query(UserModel).filter(
            UserModel.id == user_id).first()
        if not animal:
            res.errors.append(FieldError(field='animal_id',
                              message='animal does not exist'))
        if not user:
            res.errors.append(FieldError(field='user_id',
                              message='user does not exist'))
        if not res.errors:
            animal.owner_id = user_id
            db_session.commit()
            res.animal = animal
        return res


class CreateZoo(graphene.Mutation):
    class Arguments:
        input = ZooInput(required=True)

    Output = ZooResponse

    @staticmethod
    @handle_zoo_authorization_error
    @mutation_header_jwt_required
    def mutate(root, info, input):
        res = ZooResponse()
        owner = db_session.query(UserModel).filter(
            UserModel.id == input.owner_id).first()
        if not owner:
            res.errors.append(FieldError(
                field='owner_id', message='user does not exist'))
        if not res.errors:
            zoo = ZooModel(name=input.name, owner_id=input.owner_id)
            db_session.add(zoo)
            db_session.commit()
            res.zoo = zoo
        return res


class UpdateZoo(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()

    Output = ZooResponse

    @staticmethod
    @handle_zoo_authorization_error
    @mutation_header_jwt_required
    def mutate(root, info, id, name=None):
        res = ZooResponse()
        zoo = db_session.query(ZooModel).filter(
            ZooModel.id == id).first()
        if not zoo:
            res.errors.append(FieldError(
                field='id', message='zoo does not exist'))
        if not res.errors and zoo.name != name:
            zoo.name = name
            db_session.commit()
            res.zoo = zoo
        return res


class DeleteZoo(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    Output = DeleteResponse

    @ staticmethod
    @handle_zoo_authorization_error
    @ mutation_header_jwt_required
    def mutate(root, info, id):
        res = DeleteResponse()
        zoo = db_session.query(ZooModel).filter(
            ZooModel.id == id).first()
        if not zoo:
            res.errors.append(FieldError(
                field='id', message='zoo does not exist'))
        if not res.errors:
            try:
                db_session.delete(zoo)
                db_session.commit()
                res.completed = True
            except:
                pass
        return res


class TransferZoo(graphene.Mutation):
    class Arguments:
        zoo_id = graphene.Int(required=True)
        user_id = graphene.Int(required=True)

    Output = ZooResponse

    @staticmethod
    @handle_zoo_authorization_error
    @mutation_header_jwt_required
    def mutate(root, info, zoo_id, user_id):
        res = ZooResponse()
        zoo = db_session.query(ZooModel).filter(
            ZooModel.id == zoo_id).first()
        user = db_session.query(UserModel).filter(
            UserModel.id == user_id).first()
        if not zoo:
            res.errors.append(FieldError(
                field='zoo_id', message='zoo does not exist'))
        if not user:
            res.errors.append(FieldError(
                field='user_id', message='user does not exist'))
        if not res.errors:
            zoo.owner_id = user_id
            db_session.commit()
            res.zoo = zoo
        return res


class Register(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    Output = AuthResponse

    @staticmethod
    def mutate(root, info, input):
        res = AuthResponse()
        username = input.username.lower()
        user = db_session.query(UserModel).filter(
            UserModel.username == input.username).first()

        if user:
            res.errors.append(FieldError(
                field='username', message='already taken'))
        if len(username) < 3:
            res.errors.append(FieldError(field='username',
                                         message='must be at least 3 characters'))
        if len(input.password) < 3:
            res.errors.append(FieldError(field='password',
                                         message='must be at least 3 characters'))
        if not res.errors:
            hashed_password = pbkdf2_sha256.hash(input.password)
            user = UserModel(username=username,
                             password=hashed_password)
            db_session.add(user)
            db_session.commit()
            res.user = user
            res.access_token = create_access_token(username)
            res.refresh_token = create_refresh_token(username)
        return res


class Login(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    Output = AuthResponse

    @staticmethod
    def mutate(root, info, input):
        res = AuthResponse()
        username = input.username.lower()
        user = db_session.query(UserModel).filter(
            UserModel.username == username).first()
        if not user:
            res.errors.append(FieldError(field='username',
                                         message='does not exist'))
        if user and not pbkdf2_sha256.verify(input.password, user.password):
            res.errors.append(FieldError(
                field='password', message='incorrect'))
        if not res.errors:
            res.user = user
            res.access_token = create_access_token(username)
            res.refresh_token = create_refresh_token(username)
        return res


class RefreshMutation(graphene.Mutation):
    class Arguments:
        refresh_token = graphene.String()

    Output = RefreshResponse

    @handle_user_authorization_error
    @mutation_header_jwt_refresh_token_required
    def mutate(self):
        current_user = get_jwt_identity()
        return RefreshResponse(
            new_access_token=create_access_token(identity=current_user),
            new_refresh_token=create_refresh_token(identity=current_user)
        )


class Query(graphene.ObjectType):
    all_zoos = graphene.List(Zoo)

    @staticmethod
    def resolve_all_zoos(parent, info):
        return db_session.query(ZooModel).all()

    zoo = graphene.Field(Zoo)

    @staticmethod
    def resolve_zoo(parent, info, id):
        return db_session.query(ZooModel).filter(ZooModel.id == id).first()

    all_animals = graphene.List(Animal)

    @staticmethod
    def resolve_all_animals(parent, info):
        return db_session.query(AnimalModel).all()

    animal = graphene.Field(Animal)

    @staticmethod
    def resolve_animal(parent, info, id):
        return db_session.query(AnimalModel).filter(AnimalModel.id == id).first()


class Mutation(graphene.ObjectType):
    login = Login.Field()
    register = Register.Field()
    refresh = RefreshMutation.Field()

    create_zoo = CreateZoo.Field()
    update_zoo = UpdateZoo.Field()
    delete_zoo = DeleteZoo.Field()
    transfer_zoo = TransferZoo.Field()

    create_animal = CreateAnimal.Field()
    update_animal = UpdateAnimal.Field()
    delete_animal = DeleteAnimal.Field()
    move_animal = MoveAnimal.Field()
    transfer_animal = TransferAnimal.Field()


Schema = graphene.Schema(query=Query, mutation=Mutation)
