from collections.abc import MutableMapping
from typing import List
from . import Dataflow
from .internals import Map


class Output(Dataflow):
    pass


class OutputMap(Map):
    def __init__(
        self,
        names : List[str],
        outputs : List[Output],
        initializer : MutableMapping[str, Output] | None = None
    ):
        super().__init__(names, outputs, initializer)
