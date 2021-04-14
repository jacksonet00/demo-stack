from flask import Flask
from flask_graphql import GraphQLView
import os
from flask_graphql_auth import GraphQLAuth
from .schema import Schema
from .model import engine, Base


def create_app():
    app = Flask(__name__)
    app.debug = True

    app.config['SECRET_KEY'] = 'asdftyuiopasdf'
    app.config['JWT_SECRET_KEY'] = 'lkjhasdfyuop'

    # JWT_ACCESS_TOKEN_EXPIRES default = 15 minutes
    # JWT_REFRESH_TOKEN_EXPIRES default = 30 days

    auth = GraphQLAuth(app)

    Base.metadata.create_all(engine)

    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=Schema,
            graphiql=True,
        )
    )

    return app
