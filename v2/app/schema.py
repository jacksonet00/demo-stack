import graphene
from .types import (Zoo, Animal, User)
from .resolvers.animal import (animal, all_animals,
                               CreateAnimal, UpdateAnimal, DeleteAnimal, TransferAnimal, MoveAnimal)
from .resolvers.zoo import (
    all_zoos, zoo, CreateZoo, UpdateZoo, DeleteZoo, TransferZoo)
from .resolvers.user import (
    Register, RefreshMutation, Login, UploadProfilePhoto)


class Query(graphene.ObjectType):
    all_zoos = graphene.List(Zoo)

    @staticmethod
    def resolve_all_zoos(parent, info):
        return all_zoos()

    zoo = graphene.Field(Zoo)

    @staticmethod
    def resolve_zoo(parent, info, id):
        return zoo(id)

    all_animals = graphene.List(Animal)

    @staticmethod
    def resolve_all_animals(parent, info):
        return all_animals()

    animal = graphene.Field(Animal)

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
