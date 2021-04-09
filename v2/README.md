# Design Doc

## Goal

Build a GraphQL API using a PostgresSQL database, making queries via SQL Alchemy in Python, and defining my schema and resolvers in Graphene. (2) Privatize the API so that queries are protected with an authorization token which are granted to API users. (3) Containerize the server using Docker. (4) Deploy the database and containerized server to Heroku.

## Build API

- Define model in SQL Alchemy with Postgres configuration
- Split out local Postgres settings so that I can easily switch between prod and dev
- Define schema and resolvers in Graphene
- Build Flask server with /graphql endpoint