import os
from flask import Flask
from flask_graphql import GraphQLView
from flask_graphql_auth import GraphQLAuth
from .schema import Schema
from .model import engine, Base


def create_app():
    app = Flask(__name__)
    app.debug = os.environ['FLASK_DEBUG']
    app.env = os.environ['FLASK_ENV']

    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']

    # JWT_ACCESS_TOKEN_EXPIRES default = 15 minutes
    # JWT_REFRESH_TOKEN_EXPIRES default = 30 days

    GraphQLAuth(app)

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
