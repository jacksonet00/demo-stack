# import os


# class Config(object):
#     ENV = os.environ['ENV']
#     CSRF_ENABLED = True
#     SECRET_KEY = "this_is_a_secret_key"
#     # Database Configuration
#     SQLALCHEMY_TRACK_MODIFICATIONS = False


# class DevelopmentConfig(Config):
#     DEBUG = True
#     POSTGRES_DATABASE_URI = 'postgresql://jackson:password@localhost:5432/demo_stack'
#     # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + \
#     #     os.environ['DB_USERNAME'] + ':' + os.environ['DB_PASSWORD'] + \
#     #     '@' + os.environ['DB_HOST'] + ":3306/" + os.environ['DB_DATABASE']


# class ProductionConfig(Config):
#     DEBUG = False
#     POSTGRES_DATABASE_URI = 'postgresql://jackson:password@localhost:5432/demo_stack'
#     # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + \
#     #     os.environ['DB_USERNAME'] + ':' + os.environ['DB_PASSWORD'] + \
#     #     '@' + os.environ['DB_HOST'] + ":3306/" + os.environ['DB_DATABASE']
