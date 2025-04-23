from typing import List
from collections.abc import MutableMapping
from . import Data
from .internals import Map


class Parameter(Data):
    pass


class ParameterMap(Map):
    def __init__(
        self,
        names : List[str],
        values : List[Parameter],
        initializer : MutableMapping[str, Parameter] | None = None
    ):
        super().__init__(names, values, initializer)
