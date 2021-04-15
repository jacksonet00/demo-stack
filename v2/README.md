# Build Log

## Goal

(1) Build a GraphQL API in Python. (2) Privatize the API so that queries are protected with an authorization token which are granted to API users. (3) Containerize the server and database using Docker. (4) Deploy the app to Heroku. (5) Add relations to the data model. (6) Handle image uploads. (7) Scale via serverless. (8) Add documentation.

## Build API

- Define schema and resolvers in Graphene
- Build Flask server with /graphql endpoint
- Define model in SQL Alchemy with Postgres configuration
- Connect model to Graphene schema and resolvers
- Split out local Postgres settings so that I can easily switch between prod and dev

### Log

- I've gotten a flask server running a graphql endpoint. On that server I've build out all the crud operations using graphene. I have a single Animal type which I can run the crud ops on. Now I'm going to move from returning constant values from these to returning data from my database. I'll need to implement data loader as well.

- I set up a local postgres database and connected up my crud ops to the db so now I'm not returning any static data. Next thing to do is split out the settings into environment variables so I can easily switch between prod and dev.

## Add Authentication

- Flask-GraphQL-Auth (https://flask-graphql-auth.readthedocs.io/en/latest/)

### Log

- So far integrating this has been a pain in the ass, although I am doing so drunk as shit, just got back from the bar with some friends. Now I'm working on adding authentication to my little API framework. Currently I'm getting some errors when creating an access token. Update: It turned out the error was coming from breaking changes to the library from a new update to one of its dependencies. So I downgraded my version of that dependency manually and that solved my issue.

- I've gotten authentication working for a basic user class and a store object which I can protect with JWT auth using either parameters or headers. Now I just need to add these protections to animals and then get rid of the store.

- I created a login, register, and refresh mutation so that users can create accounts and get tokens.

- Now you must have a valid auth token to modify animal data, but it is publically viewable. I'm willing to say this is good enough auth for now.

## Containerize Sever

- Docker

### Log

- I found an article that reccomends an Application Factory pattern for the Flask server, so I'm going to implement that refactor. This pattern is specifically supposed to help with containerization. This is because we can generate the application and run it by running a python file which means it will be easy to add a start script for our Docker image.

- Trying to split out code into multiple files is insanely annoying in Python. Either that or it's just been so long since I learned it in Javascript that something which is complex in all languages seems simple to me only in the ones I know. Wow what a moment of enlightenment right there lol. Well hopefully I can find some better resources on this.

- I just refactored to use the app factory pattern, now I'm going to containerize the server.

- The server and database are now containerized and all features are still functional.

## Deploy App

- Heroku

### Log

- Before trying to throw my project up on Heroku, I'm spending my time figuring out Docker a bit more and understanding the right way to contain this thing. Once I understand Docker it will be much easier to follow deploy instructions.

- I think what I need to do is create a Dockerfile for both the database and the app. Then create a local.yml and production.yml for docker-compose to use. Inside of these there will be build scripts which point to the respective Dockerfile for both the server and database services. Reference github-leaderboard for a good example.

- I have docker setup very nicely now. Should be easy to deploy. I'll do that tomorrow, I've already stayed up til 1. I got lost in the code...

- I now understand the right strat for deploying. I have everything setup, but I'm still getting some bugs when deploying. I went ahead and moved everything into environment variables and created start, stop, debug, and deploy scripts.

- The app is now deployed on Heroku. It could use a bit of cleanup to reduce env vars and what not, but for now it is functional.

## Add Relations

**Refactor app:**

- manage.py
- app (3. intializes base class)
  - schema.py (2. imports resolvers)
  - engine.py (1. base class passed to models)
  - data
    - user
      - model.py
      - resolver.py
    - zoo
      - model.py
      - resolver.py
    - animal
      - model.py
      - resolver.py
    - types

**New Model:**

- User(username: text, password: text)

  - id: Int
  - username: String
  - zoos: [Zoo]
  - animals: [Animal]

- Zoo(name: text, owner_id: int)

  - id: Int
  - name: String
  - ownerId: Int
  - owner: User
  - animals: [Animal]

- Animal(name: text, owner_id: int, zoo_id: nullable int)
  - id: Int
  - ownerId: Int
  - owner: User
  - zooId: Int?
  - zoo: Zoo?

### Log

- I'm honestly so happy with how this has been going so far. Never would have expected it to be this smooth. And when I run into issues I'm actually investing the time to fully understand the problem so that I learn more about configuring the stack.

- Refactor is looking really, really clean. Still a couple bugs, stuck on this one right now:

  ```
  Traceback (most recent call last):
  server_1  |   File "manage.py", line 3, in <module>
  server_1  |     from app import create_app
  server_1  |   File "/usr/src/app/app/__init__.py", line 5, in <module>
  server_1  |     from .schema import Schema
  server_1  |   File "/usr/src/app/app/schema.py", line 47, in <module>
  server_1  |     Schema = graphene.Schema(query=Query, mutation=Mutation)
  server_1  |   File "/usr/local/lib/python3.8/site-packages/graphene/types/schema.py", line 78, in __init__
  server_1  |     self.build_typemap()
  server_1  |   File "/usr/local/lib/python3.8/site-packages/graphene/types/schema.py", line 167, in build_typemap
  server_1  |     self._type_map = TypeMap(
  server_1  |   File "/usr/local/lib/python3.8/site-packages/graphene/types/typemap.py", line 80, in __init__
  server_1  |     super(TypeMap, self).__init__(types)
  server_1  |   File "/usr/local/lib/python3.8/site-packages/graphql/type/typemap.py", line 31, in __init__
  server_1  |     self.update(reduce(self.reducer, types, OrderedDict()))  # type: ignore
  server_1  |   File "/usr/local/lib/python3.8/site-packages/graphene/types/typemap.py", line 88, in reducer
  server_1  |     return self.graphene_reducer(map, type)
  server_1  |   File "/usr/local/lib/python3.8/site-packages/graphene/types/typemap.py", line 117, in graphene_reducer
  server_1  |     return GraphQLTypeMap.reducer(map, internal_type)
  server_1  |   File "/usr/local/lib/python3.8/site-packages/graphql/type/typemap.py", line 109, in reducer
  server_1  |     field_map = type_.fields
  server_1  |   File "/usr/local/lib/python3.8/site-packages/graphql/pyutils/cached_property.py", line 22, in __get__
  server_1  |     value = obj.__dict__[self.func.__name__] = self.func(obj)
  server_1  |   File "/usr/local/lib/python3.8/site-packages/graphql/type/definition.py", line 198, in fields
  server_1  |     return define_field_map(self, self._fields)
  server_1  |   File "/usr/local/lib/python3.8/site-packages/graphql/type/definition.py", line 212, in define_field_map
  server_1  |     field_map = field_map()
  server_1  |   File "/usr/local/lib/python3.8/site-packages/graphene/types/typemap.py", line 275, in construct_fields_for_type
  server_1  |     map = self.reducer(map, field.type)
  server_1  |   File "/usr/local/lib/python3.8/site-packages/graphene/types/typemap.py", line 88, in reducer
  server_1  |     return self.graphene_reducer(map, type)
  server_1  |   File "/usr/local/lib/python3.8/site-packages/graphene/types/typemap.py", line 93, in graphene_reducer
  server_1  |     return self.reducer(map, type.of_type)
  server_1  |   File "/usr/local/lib/python3.8/site-packages/graphene/types/typemap.py", line 88, in reducer
  server_1  |     return self.graphene_reducer(map, type)
  server_1  |   File "/usr/local/lib/python3.8/site-packages/graphene/types/typemap.py", line 117, in graphene_reducer
  server_1  |     return GraphQLTypeMap.reducer(map, internal_type)
  server_1  |   File "/usr/local/lib/python3.8/site-packages/graphql/type/typemap.py", line 109, in reducer
  server_1  |     field_map = type_.fields
  server_1  |   File "/usr/local/lib/python3.8/site-packages/graphql/pyutils/cached_property.py", line 22, in __get__
  server_1  |     value = obj.__dict__[self.func.__name__] = self.func(obj)
  server_1  |   File "/usr/local/lib/python3.8/site-packages/graphql/type/definition.py", line 198, in fields
  server_1  |     return define_field_map(self, self._fields)
  server_1  |   File "/usr/local/lib/python3.8/site-packages/graphql/type/definition.py", line 212, in define_field_map
  server_1  |     field_map = field_map()
  server_1  |   File "/usr/local/lib/python3.8/site-packages/graphene/types/typemap.py", line 275, in construct_fields_for_type
  server_1  |     map = self.reducer(map, field.type)
  server_1  |   File "/usr/local/lib/python3.8/site-packages/graphene/types/typemap.py", line 89, in reducer
  server_1  |     return GraphQLTypeMap.reducer(map, type)
  server_1  |   File "/usr/local/lib/python3.8/site-packages/graphql/type/typemap.py", line 87, in reducer
  server_1  |     if type_.name in map_:
  server_1  | AttributeError: module 'app.api.user' has no attribute 'name'
  ```
