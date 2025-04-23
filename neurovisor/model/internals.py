from abc import abstractmethod, ABC
from collections import defaultdict
from typing import Any, Iterable

import json


class Serializable(ABC):
    @abstractmethod
    def serialize(self):
        pass

    def __repr__(self):
        return json.dumps(self.serialize())


class Map(Serializable, defaultdict):
    can_be_empty = False

    def __init__(
        self,
        names : Iterable[Any],
        values : Iterable[Any],
        initializer : dict | None = None
    ):
        super().__init__()

        if not self.can_be_empty and all([
            n is None for n in [names, values, initializer]
        ]):
            raise ValueError("At least both names and values, "
                             "or initializer must be provided.")

        if initializer is not None:
            self.update(initializer)

        if names is not None and values is not None:
            self.update(zip(names, values))

    def serialize(self):
        return {k: v.serialize() for k, v in self.items()}
