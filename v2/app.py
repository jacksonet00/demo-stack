from flask import Flask
from flask_graphql import GraphQLView
from schema import schema
import os
from flask_graphql_auth import GraphQLAuth

app = Flask(__name__)
app.debug = os.environ.get('DEBUG')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

# JWT_ACCESS_TOKEN_EXPIRES default = 15 minutes
# JWT_REFRESH_TOKEN_EXPIRES default = 30 days

auth = GraphQLAuth(app)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
    )
)

if __name__ == '__main__':
    app.run()