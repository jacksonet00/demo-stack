import graphene
from ..engine import db_session
from ..model import (User as UserModel, Zoo as ZooModel, Animal as AnimalModel)
from ..types import (AnimalInput, AnimalResponse, FieldError, DeleteResponse)
from ..auth import (is_auth, get_identity)
from datetime import datetime


def all_animals(limit, cursor):
    real_limit = min(50, limit)
    q = db_session.query(AnimalModel)

    if cursor:
        real_cursor = datetime.strptime(cursor, '%Y-%m-%d %H:%M:%S')
        q = q.filter(AnimalModel.created_at < real_cursor)

    return q.order_by(
        AnimalModel.created_at.desc()).limit(real_limit).all()


def animal(id):
    return db_session.query(AnimalModel).filter(AnimalModel.id == id).first()


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
