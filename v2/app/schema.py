import graphene
from .types import (Zoo, PaginatedZoos, Animal, PaginatedAnimals, User)
from .resolvers import (animal, all_animals, CreateAnimal, UpdateAnimal, DeleteAnimal, TransferAnimal, MoveAnimal,
                        all_zoos, zoo, CreateZoo, UpdateZoo, DeleteZoo, TransferZoo, Register, RefreshMutation, Login, UploadProfilePhoto)


class Query(graphene.ObjectType):
    all_zoos = graphene.Field(PaginatedZoos, limit=graphene.Int(),
                              cursor=graphene.String())

    @staticmethod
    def resolve_all_zoos(parent, info, limit=50, cursor=None):
        return all_zoos(limit, cursor)

    zoo = graphene.Field(Zoo, id=graphene.Int(required=True))

    @staticmethod
    def resolve_zoo(parent, info, id):
        return zoo(id)

    all_animals = graphene.Field(
        PaginatedAnimals, limit=graphene.Int(), cursor=graphene.String())

    @staticmethod
    def resolve_all_animals(parent, info, limit=50, cursor=None):
        return all_animals(limit, cursor)

    animal = graphene.Field(Animal, id=graphene.Int(required=True))

    @staticmethod
    def resolve_animal(parent, info, id):
        return animal(id)


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


Schema = graphene.Schema(query=Query, mutation=Mutation)
