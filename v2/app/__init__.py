import os
from flask import Flask, redirect
from flask_graphql import GraphQLView
from flask_graphql_auth import GraphQLAuth
from .schema import Schema
from .engine import engine, Base


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'asdfhasdjhfkja'
    app.config['JWT_SECRET_KEY'] = os.environ.get(
        'JWT_SECRET_KEY') or 'ajsdfgaksdbbjknv'

    app.debug = False if os.environ.get('ENV') == '__prod__' else True

    # JWT_ACCESS_TOKEN_EXPIRES default = 15 minutes
    # JWT_REFRESH_TOKEN_EXPIRES default = 30 days

    GraphQLAuth(app)

    Base.metadata.create_all(engine)

    # pylint: disable=unused-variable
    @app.route('/')
    def index():
        return redirect('/graphql')

    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=Schema,
            graphiql=True,
        )
    )

    return app
