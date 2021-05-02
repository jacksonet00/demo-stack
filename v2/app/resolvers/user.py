import graphene
from graphene_file_upload.scalars import Upload
from passlib.hash import pbkdf2_sha256
from ..types import (UserInput, AuthResponse, FieldError,
                     RefreshResponse, UserResponse)
from ..engine import db_session
from ..model import User as UserModel
from ..auth import (create_access_token,
                    create_refresh_token, get_identity, is_auth)
from ..cloud import (get_path, upload_to_gcloud)


def me(info):
    if not is_auth(info):
        return UserResponse(errors=[FieldError(field='headers[Authorization]', message='invalid access token')])
    res = UserResponse(errors=[])
    if not res.errors:
        user = UserModel.query.filter(
            UserModel.username == get_identity(info)).first()
        res.user = user
    return res


class Register(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    Output = AuthResponse

    @staticmethod
    def mutate(root, info, input):
        res = AuthResponse()
        username = input.username.lower()
        user = UserModel.query.filter(
            UserModel.username == input.username).first()

        if user:
            res.errors.append(FieldError(
                field='username', message='already taken'))
        if len(username) < 3:
            res.errors.append(FieldError(field='username',
                                         message='must be at least 3 characters'))
        if len(input.password) < 3:
            res.errors.append(FieldError(field='password',
                                         message='must be at least 3 characters'))
        if not res.errors:
            hashed_password = pbkdf2_sha256.hash(input.password)
            user = UserModel(username=username,
                             password=hashed_password)
            db_session.add(user)
            db_session.commit()
            res.user = user
            res.access_token = create_access_token(username)
            res.refresh_token = create_refresh_token(username)
        return res


class Login(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    Output = AuthResponse

    @staticmethod
    def mutate(root, info, input):
        res = AuthResponse()
        username = input.username.lower()
        user = UserModel.query.filter(
            UserModel.username == username).first()
        if not user:
            res.errors.append(FieldError(field='username',
                                         message='does not exist'))
        if user and not pbkdf2_sha256.verify(input.password, user.password):
            res.errors.append(FieldError(
                field='password', message='incorrect'))
        if not res.errors:
            res.user = user
            res.access_token = create_access_token(username)
            res.refresh_token = create_refresh_token(username)
        return res


class RefreshMutation(graphene.Mutation):
    class Arguments:
        pass

    Output = RefreshResponse

    @classmethod
    def mutate(self, info):
        username = get_identity(info)
        return RefreshResponse(
            new_access_token=create_access_token(username),
            new_refresh_token=create_refresh_token(username)
        )


class UploadProfilePhoto(graphene.Mutation):
    class Arguments:
        photo = Upload(required=True)

    Output = UserResponse

    def mutate(self, info, photo, **kwargs):
        if not is_auth(info):
            return UserResponse(errors=[FieldError(field='headers[Authorization]', message='invalid token')])

        res = UserResponse(errors=[])

        user = UserModel.query.filter(
            UserModel.username == get_identity(info)).first()

        if not res.errors:
            try:
                path = get_path(photo.filename, username=user.username)
                try:
                    upload = upload_to_gcloud(
                        bucket_name='demo-stack-uploads', file=photo, file_path=path)
                    user.profile_photo = upload['url']
                    db_session.commit()
                    res.user = user
                except:
                    res.errors.append(FieldError(
                        field='photo', message='upload failed'))
            except Exception as e:
                error = str(e).split('|')
                res.errors.append(FieldError(field=error[0], message=error[1]))

        return res
