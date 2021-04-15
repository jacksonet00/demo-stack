import graphene
from flask_graphql_auth import create_access_token, create_refresh_token, get_jwt_identity, mutation_header_jwt_required, mutation_header_jwt_refresh_token_required
from passlib.hash import pbkdf2_sha256
from ...engine import db_session
from ..user.model import User as UserModel
from ..types.response import AuthResponse, RefreshResponse
from ..types.user import UserInput
from ..types.error import FieldError
from ...tools import handle_user_authorization_error


class Register(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    Output = AuthResponse

    @staticmethod
    def mutate(root, info, input):
        res = AuthResponse()

        user = db_session.query(UserModel).filter(
            UserModel.username == input.username).first()

        if user:
            res.errors.append(FieldError(
                field='username', message='already taken'))
        if len(input.username) < 3:
            res.errors.append(FieldError(field='username',
                                         message='must be at least 3 characters'))
        if len(input.password) < 3:
            res.errors.append(FieldError(field='password',
                                         message='must be at least 3 characters'))
        if not res.errors:
            hashed_password = pbkdf2_sha256.hash(input.password)
            user = UserModel(username=input.username,
                             password=hashed_password)
            db_session.add(user)
            db_session.commit()
            res.user = user
            res.access_token = create_access_token(input.username)
            res.refresh_token = create_refresh_token(input.username)
        return res


class Login(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    Output = AuthResponse

    @staticmethod
    def mutate(root, info, input):
        res = AuthResponse()
        user = db_session.query(UserModel).filter(
            UserModel.username == input.username).first()
        if not user:
            res.errors.append(FieldError(field='username',
                                         message='does not exist'))
        if user and not pbkdf2_sha256.verify(input.password, user.password):
            res.errors.append(FieldError(
                field='password', message='incorrect'))
        if not res.errors:
            res.user = user
            res.access_token = create_access_token(input.username)
            res.refresh_token = create_refresh_token(input.username)
        return res


class RefreshMutation(graphene.Mutation):
    class Arguments:
        refresh_token = graphene.String()

    Output = RefreshResponse

    @handle_user_authorization_error
    @mutation_header_jwt_refresh_token_required
    def mutate(self):
        current_user = get_jwt_identity()
        return RefreshResponse(
            new_access_token=create_access_token(identity=current_user),
            new_refresh_token=create_refresh_token(identity=current_user)
        )
