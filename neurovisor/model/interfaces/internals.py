from collections import UserDict
from typing import Any, Iterable


class Map(UserDict):
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
