from ..constants import PROTECTED_QUERIES
from .jwt import is_auth


class AuthorizationMiddleware:
    def resolve(self, next, root, info, **args):
        if info.field_name in PROTECTED_QUERIES:
            if is_auth(info):
                return next(root, info, **args)
            else:
                raise Exception('Invalid Authorization token.')
        else:
            return next(root, info, **args)
