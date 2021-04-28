import graphene
from passlib.hash import pbkdf2_sha256
from graphene_file_upload.scalars import Upload
from .types import (FieldError, UserInput, RefreshResponse,
                    AnimalInput, ZooInput, DeleteResponse)
from .engine import db_session
from .model import (Animal as AnimalModel, Zoo as ZooModel, User as UserModel)
from .cloud import (upload_to_gcloud, get_path)
from .auth import create_access_token, create_refresh_token, get_identity, is_auth


class FileUpload(graphene.ObjectType):
    url = graphene.String()
    owner_id = graphene.Int()
    owner = graphene.Field(lambda: User)

    @staticmethod
    def resolve_owner(parent, info):
        return db_session.query(UserModel).filter(UserModel.id == parent.owner_id).first()


class UploadResponse(graphene.ObjectType):
    fileUpload = graphene.Field(FileUpload, default_value=None)
    errors = graphene.List(FieldError, default_value=[])


class UploadMutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    Output = UploadResponse

    def mutate(self, info, file, **kwargs):
        res = UploadResponse()
        owner = db_session.query(UserModel).filter(
            UserModel.username == get_identity(info)).first()
        if not owner:
            res.errors.append(FieldError(field='Authorization Header',
                              message='User does not exist'))
        if not res.errors:
            try:
                path = get_path(file.filename, username=owner.username)
                try:
                    # TODO: move bucket name to env var
                    upload = upload_to_gcloud(
                        bucket_name='demo-stack-uploads', file=file, file_path=path)
                    res.fileUpload = FileUpload(
                        url=upload['url'], owner_id=owner.id)
                except:
                    res.errors.append(FieldError(
                        field='file', message='upload failed'))
            except Exception as e:
                error = str(e).split('|')
                res.errors.append(FieldError(field=error[0], message=error[1]))
        return res


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
    profile_photo = graphene.String(required=False)
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()


class UserResponse(graphene.ObjectType):
    user = graphene.Field(User, default_value=None)
    errors = graphene.List(FieldError, default_value=[])


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
    def mutate(root, info, input):
        if not is_auth(info):
            return AnimalResponse(errors=[FieldError(
                field='headers[Authorization]', message='invalid access token')])

        res = AnimalResponse(errors=[])

        owner = db_session.query(UserModel).filter(
            UserModel.username == get_identity(info)).first()

        if input.zoo_id:
            zoo = db_session.query(ZooModel).filter(
                ZooModel.id == input.zoo_id).first()
            if not zoo:
                res.errors.append(FieldError(
                    field='zooId', message='zoo does not exist'))

        if not res.errors:
            animal = AnimalModel(name=input.name, owner_id=owner.id)
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
    def mutate(root, info, id, name=None):
        if not is_auth(info):
            return AnimalResponse(errors=[FieldError(
                field='headers[Authorization]', message='invalid access token')])
        res = AnimalResponse(errors=[])
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
    def mutate(root, info, id):
        if not is_auth(info):
            return DeleteResponse(errors=[FieldError(
                field='headers[Authorization]', message='invalid access token')])
        res = DeleteResponse(errors=[])
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
    def mutate(root, info, animal_id, zoo_id):
        if not is_auth(info):
            return AnimalResponse(errors=[FieldError(
                field='headers[Authorization]', message='invalid access token')])
        res = AnimalResponse(errors=[])
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
    def mutate(root, info, animal_id, user_id):
        if not is_auth(info):
            return AnimalResponse(errors=[FieldError(
                field='headers[Authorization]', message='invalid access token')])
        res = AnimalResponse(errors=[])
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
    def mutate(root, info, input):
        if not is_auth(info):
            return ZooResponse(errors=[FieldError(
                field='headers[Authorization]', message='invalid access token')])
        res = ZooResponse(errors=[])
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
    def mutate(root, info, id, name=None):
        if not is_auth(info):
            return ZooResponse(errors=[FieldError(
                field='headers[Authorization]', message='invalid access token')])
        res = ZooResponse(errors=[])
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
    def mutate(root, info, id):
        if not is_auth(info):
            return DeleteResponse(errors=[FieldError(
                field='headers[Authorization]', message='invalid access token')])
        res = DeleteResponse(errors=[])
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
    def mutate(root, info, zoo_id, user_id):
        if not is_auth(info):
            return ZooResponse(errors=[FieldError(
                field='headers[Authorization]', message='invalid access token')])
        res = ZooResponse(errors=[])
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
        pass

    Output = RefreshResponse

    @classmethod
    def mutate(self, info):
        username = get_identity(info)
        return RefreshResponse(
            new_access_token=create_access_token(username),
            new_refresh_token=create_refresh_token(username)
        )


class UploadProfilePhoto(graphene.Mutation):
    class Arguments:
        photo = Upload(required=True)

    Output = UserResponse

    def mutate(self, info, photo, **kwargs):
        if not is_auth(info):
            return UserResponse(errors=[FieldError(field='headers[Authorization]', message='invalid token')])

        res = UserResponse(errors=[])

        user = db_session.query(UserModel).filter(
            UserModel.username == get_identity(info)).first()

        if not res.errors:
            try:
                path = get_path(photo.filename, username=user.username)
                try:
                    upload = upload_to_gcloud(
                        bucket_name='demo-stack-uploads', file=photo, file_path=path)
                    user.profile_photo = upload['url']
                    db_session.commit()
                    res.user = user
                except:
                    res.errors.append(FieldError(
                        field='photo', message='upload failed'))
            except Exception as e:
                error = str(e).split('|')
                res.errors.append(FieldError(field=error[0], message=error[1]))

        return res


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
    upload_profile_photo = UploadProfilePhoto.Field()

    create_zoo = CreateZoo.Field()
    update_zoo = UpdateZoo.Field()
    delete_zoo = DeleteZoo.Field()
    transfer_zoo = TransferZoo.Field()

    create_animal = CreateAnimal.Field()
    update_animal = UpdateAnimal.Field()
    delete_animal = DeleteAnimal.Field()
    move_animal = MoveAnimal.Field()
    transfer_animal = TransferAnimal.Field()

    upload_file = UploadMutation.Field()


Schema = graphene.Schema(query=Query, mutation=Mutation)
