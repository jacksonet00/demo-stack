import graphene

class Animal(graphene.ObjectType):
  id = graphene.Int()
  name = graphene.String()
  computed_name = graphene.String()

  @staticmethod
  def resolve_computed_name(parent, info):
    return f'{parent.name}-007'

class AnimalInput(graphene.InputObjectType):
  name = graphene.String(required=True)

class InputError(graphene.ObjectType):
  field = graphene.String()
  message = graphene.String()

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
  def mutate(root, info, input=None):
    output = AnimalOutput()
    if len(input.name) < 3:
      output.errors.append(InputError(field='name', message='must be at least 3 characters'))
    if not output.errors:
      output.animal = Animal(id=1, name=input.name)
    return output

class UpdateAnimal(graphene.Mutation):
  class Arguments:
    id = graphene.Int()
    name = graphene.String()

  Output = AnimalOutput

  @staticmethod
  def mutate(root, info, id=None, name=None):
    output = AnimalOutput()
    errors = []
    if id not in [1, 2]:
      errors.append(InputError(field='id', message='not found'))
    if len(name) < 3:
      errors.append(InputError(field='name', message='must be at least 3 characters'))
    output.errors = errors
    if not errors:
      output.animal = Animal(id=id, name=name)
    return output

class DeleteAnimal(graphene.Mutation):
  class Arguments:
    id = graphene.Int()

  Output = DeleteOutput

  @staticmethod
  def mutate(root, info, id):
    output = DeleteOutput()
    if id not in [1, 2]:
      output.errors.append(InputError(field='id', message='not found'))
    if not output.errors:
      output.completed = True
    return output

class Query(graphene.ObjectType):
  animal = graphene.Field(Animal)
  all_animals = graphene.List(Animal)

  @staticmethod
  def resolve_all_animals(parent, info):
    return [Animal(id=1, name='tiger'), Animal(id=2, name='lion')]

  @staticmethod
  def resolve_animal(parent, info):
    a = Animal(id=1, name='tiger')
    return a

class Mutation(graphene.ObjectType):
  create_animal = CreateAnimal.Field()
  update_animal = UpdateAnimal.Field()
  delete_animal = DeleteAnimal.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)