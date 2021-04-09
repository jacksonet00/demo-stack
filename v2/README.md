# Design Doc

## Goal

Build a GraphQL API using a PostgresSQL database, making queries via SQL Alchemy in Python, and defining my schema and resolvers in Graphene. (2) Privatize the API so that queries are protected with an authorization token which are granted to API users. (3) Containerize the server using Docker. (4) Deploy the database and containerized server to Heroku.

## Build API

- Define model in SQL Alchemy with Postgres configuration
- Split out local Postgres settings so that I can easily switch between prod and dev
- Define schema and resolvers in Graphene
- Build Flask server with /graphql endpoint

### Log

- I've gotten a flask server running a graphql endpoint. On that server I've build out all the crud operations using graphene. I have a single Animal type which I can run the crud ops on. Now I'm going to move from returning constant values from these to returning data from my database. I'll need to implement data loader as well.