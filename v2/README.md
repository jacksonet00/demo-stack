# Build Log

## Goal

(1) Build a GraphQL API in Python. (2) Privatize the API. (3) Containerize the server and database using Docker. (4) Deploy the app to Heroku. (5) Add relations to the data model. (6) Handle image uploads. (7) Add pagination. (8) Add dataloader. (9) Add session management with Redis. (10) Rate limiting. (11) DDoS protection. (12) Tests

Hosted at: https://demo-stack.herokuapp.com/graphql

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

- manage
- app
  - schema
  - engine
  - types
  - model

**New Model:**

- User(input: { username: String!, password: String! })

  - id: Int
  - username: String
  - zoos: [Zoo]
  - animals: [Animal]

- Zoo(input: { name: String!, ownerId: Int! })

  - id: Int
  - name: String
  - ownerId: Int
  - owner: User
  - animals: [Animal]

- Animal(input: { name: String!, ownerId: Int!, zooId: Int? })

  - id: Int
  - ownerId: Int
  - owner: User
  - zooId: Int?
  - zoo: Zoo?

**Mutations:**

- User
  - Register(input: { username: String!, password: String! })
  - Login(input: { username: String!, password: String! })
  - Refresh(refreshToken: String!)
- Animal
  - CRUD
  - Move(animalId: Int!, zooId: Int!)
  - Transfer(animalId: Int!, userId: Int!)
- Zoo
  - CRUD
  - Transfer(zooId: Int!, userId: Int!)

### Log

- I'm honestly so happy with how this has been going so far. Never would have expected it to be this smooth. And when I run into issues I'm actually investing the time to fully understand the problem so that I learn more about configuring the stack.

- I've got the new schema setup and the new mutations added. Before moving on to image uploads I'm going to try to get the user mutations working a little better. I want to have a full auth setup where you create an account, confirm an email or phone number, login, and then the app can detect who you are based off of your access token.

- Everything seems to be working, didn't get around to improving the auth system. I'll probably get image uploads, pagination, and dataloader working first. Then I'll improve the auth before moving on to the deploy system. At that same time I'll probably refactor to use `SQLAlchemyObjectType` and `relay`.

## Handle Image Uploads

- graphene-file-upload
- Google Cloud Storage

**Steps**

1. Implement graphene-file-upload
2. Upload files via postman to local folder
3. Swap out local folder for GCP bucket using google-cloud-storage
4. Configure bucket permissions
5. Add profile images to User

**Stretch**

6. Layer imigix in front of GCP for resizing

### Log

- Currently I've implemented the graphene-file-upload library and I have a local images folder which I can push files to through graphql. Next step is to clean up this system a bit and then switch out the local folder for a GCP bucket.

- Now I have a system setup where you can upload a file and it will be saved to Google Cloud. I'm going to work on making this a bit more robust and also on learning more about GCP.

- The auth system is causing some annoying issues. Having this in a wrapper rather than a function, or some middleware is not ideal. I'm going to look into swapping out the auth for a different solution. I'm also going to add a Me query and rework all the resolvers to use the new auth system and infer user_id from the JWT.

- I implemented my own auth system. It's a lot cleaner and easier to manage than flask-graphql-auth, I'm going to rip that one out.

- I implemented profile photos for users. I think I'm good to move on from file uploads now, I'm saving the stretch goal since it has a monthly cost associated with it.

## Add Pagination

- Modify fetch queries to select with a limit
- Modify fetch queries to order by created_at
- Use cursor to filter by less than created_at

### Log

- No idea how to do this atm. I'm going to watch a video of someone implementing it in Typescript and see if I can figure it out in Python on my own.

- So I am adding cursor-based pagination to the fetch queries. You will pass a limit and a cursor where the limit is the number of items you want to fetch and cursor is the created_at date you want to fetch from where the items are sorted by newest.

- For now I'm not going to refactor into the Graphene-SQLAlchemy library with the SQLAlchemyObjectType. I'm not a fan of the API for it and it has some limitations as I understand it currently. If I find a way to bypass these limitations, then I'll reconsider implementing. Maybe using some abstraction snippets I found online that make the API a bit cleaner. IMO it isn't worth it to add an abstraction if it won't actually benefit the cleanliness and flexibility of your code.

- Completed cursor based pagination. Implemented it on allAnimals and allZoos.

## Add Dataloader

- Extend dataloader class from promise library
- Use as the resolver function for nested objects

### Log

- Dataloader is now implemented. That was quite easy!

## Session Management

- Redis
- JWT

### Log

- I have been thinking about this for a couple weeks now and I still don't fully conceptualize auth + sessions + cookies + jwts.

- I'm going to have to make changes to the deploy set up in order to intergrate redis, so before getting started with that I'm going to make sure everything currently is deploying correctly so that I'm only changing 1 element at a time.
