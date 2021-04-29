import graphene
from ..types import (ZooInput, ZooResponse, FieldError, DeleteResponse)
from ..engine import db_session
from ..model import (User as UserModel, Zoo as ZooModel)
from ..auth import is_auth


def all_zoos():
    return db_session.query(ZooModel).all()


def zoo(id):
    return db_session.query(ZooModel).filter(ZooModel.id == id).first()


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
