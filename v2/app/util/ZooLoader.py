from promise import Promise
from promise.dataloader import DataLoader
from ..model import Zoo as ZooModel


class ZooLoader(DataLoader):
    # pylint: disable = method-hidden
    def batch_load_fn(self, keys):
        zoos = {zoo.id: zoo for zoo in ZooModel.query.filter(
            ZooModel.id.in_(keys)).all()}
        return Promise.resolve([zoos.get(key) for key in keys])
