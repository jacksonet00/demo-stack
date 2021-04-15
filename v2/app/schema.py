import graphene
from .api.user.resolver import Login, Register, RefreshMutation
from .api.zoo import Zoo, resolver as zoo_resolver
from .api.animal import Animal, resolver as animal_resolver


class Query(graphene.ObjectType):
    all_zoos = graphene.List(Zoo)

    @staticmethod
    def resolve_all_zoos(parent, info):
        return zoo_resolver.all_zoos()

    zoo = graphene.Field(Zoo)

    @staticmethod
    def resolve_zoo(parent, info, id):
        return zoo_resolver.zoo(id)

    all_animals = graphene.List(Animal)

    @staticmethod
    def resolve_all_animals(parent, info):
        return animal_resolver.all_animals()

    animal = graphene.Field(Animal)

    @staticmethod
    def resolve_animal(parent, info, id):
        return animal_resolver.animal(id)


class Mutation(graphene.ObjectType):
    login = Login.Field()
    register = Register.Field()
    refresh = RefreshMutation.Field()

    create_zoo = zoo_resolver.CreateZoo.Field()
    update_zoo = zoo_resolver.UpdateZoo.Field()
    delete_zoo = zoo_resolver.DeleteZoo.Field()

    create_animal = animal_resolver.CreateAnimal.Field()
    update_animal = animal_resolver.UpdateAnimal.Field()
    delete_zoo = animal_resolver.DeleteAnimal.Field()


Schema = graphene.Schema(query=Query, mutation=Mutation)
