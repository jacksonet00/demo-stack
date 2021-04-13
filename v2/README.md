# Design Doc

## Goal

Build a GraphQL API using a PostgresSQL database, making queries via SQL Alchemy in Python, and defining my schema and resolvers in Graphene. (2) Privatize the API so that queries are protected with an authorization token which are granted to API users. (3) Containerize the server using Docker. (4) Deploy the database and containerized server to Heroku. (5) Add relations to the data model. (6) Handle image uploads. (7) Scale via serverless.

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

- Trying to split out code into multiple files is insanely annoying in Python. Either that or it's just been so long since I learned it in Javascript that something which is complex in all languages seems simple to me only in  the ones I know. Wow what a moment of enlightenment right there lol. Well hopefully I can find some better resources on this.