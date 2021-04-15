import graphene
from ...engine import db_session
from ..animal.model import Animal as AnimalModel
from ..animal import Animal
from ..types.error import FieldError
from ...tools import handle_animal_authorization_error
from flask_graphql_auth import mutation_header_jwt_required
from ..user.model import User as UserModel
from ..zoo.model import Zoo as ZooModel
from ..types.response import DeleteResponse
from ..types.animal import AnimalResponse, AnimalInput


def all_animals():
    return db_session.query(AnimalModel).all()


def animal(id):
    return db_session.query(AnimalModel).filter(AnimalModel.id == id).first()


class CreateAnimal(graphene.Mutation):
    class Arguments:
        input = AnimalInput(required=True)

    Output = AnimalInput

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
