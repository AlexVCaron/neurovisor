from typing import List
from collections.abc import MutableMapping
from . import Data
from .internals import Map


class Parameter(Data):
    pass


class ParameterMap(Map):
    def __init__(
        self,
        names : List[str] | None = None,
        values : List[Parameter] | None = None,
        initializer : MutableMapping[str, Parameter] | None = None
    ):
        self.can_be_empty = True
        super().__init__(names, values, initializer)
