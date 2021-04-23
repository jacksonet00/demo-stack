import os
from flask import Flask, redirect
# from flask_graphql import GraphQLView
from graphene_file_upload.flask import FileUploadGraphQLView
from flask_graphql_auth import GraphQLAuth
from .schema import Schema
from .engine import engine, Base
import json
from .db import gen_data, drop_tables


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'asdfhasdjhfkja')
    app.config['JWT_SECRET_KEY'] = os.environ.get(
        'JWT_SECRET_KEY', 'ajsdfgaksdbbjknv')

    # JWT_ACCESS_TOKEN_EXPIRES default = 15 minutes
    # JWT_REFRESH_TOKEN_EXPIRES default = 30 days

    app.debug = os.environ.get('ENV') != '__prod__'

    GraphQLAuth(app)

    drop_tables(['animals', 'zoos', 'users'])

    Base.metadata.create_all(engine)

    # Generate dummy data for dev environment
    if os.environ.get('ENV') == '__dev__':
        gen_data()

    # pylint: disable=unused-variable
    @app.route('/')
    def index():
        return json.dumps({'message': 'help me! i am trapped making this api!'})

    app.add_url_rule(
        '/graphql',
        view_func=FileUploadGraphQLView.as_view(
            'graphql',
            schema=Schema,
            graphiql=True,
        )
    )

    return app
