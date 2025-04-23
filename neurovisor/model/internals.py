from abc import abstractmethod, ABC
from collections import UserDict
from typing import Any, Iterable

import json


class Serializable(ABC):
    @abstractmethod
    def serialize(self):
        pass

    @classmethod
    @abstractmethod
    def read(*args, **kwargs):
        pass

    def __repr__(self):
        return json.dumps(self.serialize())


class Map(Serializable, UserDict):
    def __init__(
        self,
        names : Iterable[Any],
        values : Iterable[Any],
        initializer : dict | None = None
    ):
        super().__init__()

        if initializer is not None:
            self.update(initializer)

        if names is not None and values is not None:
            self.update(zip(names, values))

    def serialize(self):
        return self
