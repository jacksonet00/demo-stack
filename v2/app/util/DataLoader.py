from promise import Promise
from promise.dataloader import DataLoader
from ..model import (User as UserModel, Zoo as ZooModel)


class UserLoader(DataLoader):
    # pylint: disable = method-hidden
    def batch_load_fn(self, keys):
        users = {user.id: user for user in UserModel.query.filter(
            UserModel.id.in_(keys)).all()}
        return Promise.resolve([users.get(key) for key in keys])


class ZooLoader(DataLoader):
    # pylint: disable = method-hidden
    def batch_load_fn(self, keys):
        zoos = {zoo.id: zoo for zoo in ZooModel.query.filter(
            ZooModel.id.in_(keys)).all()}
        return Promise.resolve([zoos.get(key) for key in keys])
