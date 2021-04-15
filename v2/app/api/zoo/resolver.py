import graphene
from ...engine import db_session
from .model import Zoo as ZooModel
from . import Zoo
from ...tools import handle_zoo_authorization_error
from flask_graphql_auth import mutation_header_jwt_required
from ..types.error import FieldError
from ..user.model import User as UserModel
from ..types.response import DeleteResponse
from ..types.zoo import ZooInput, ZooResponse


def all_zoos():
    return db_session.query(ZooModel).all()


def zoo(id):
    return db_session.query(ZooModel).filter(ZooModel.id == id).first()


class CreateZoo(graphene.Mutation):
    class Arguments:
        input = ZooInput(required=True)

    Output = ZooInput

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
