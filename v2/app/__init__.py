import os
from flask import Flask, redirect
from graphene_file_upload.flask import FileUploadGraphQLView
from .schema import Schema
from .engine import engine, Base
import json
from .db import gen_data, drop_tables
from .auth import AuthorizationMiddleware


def create_app():  # App Factory
    app = Flask(__name__)
    app.debug = os.environ.get('ENV') != '__prod__'

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
            middleware=[AuthorizationMiddleware()]
        )
    )

    return app
