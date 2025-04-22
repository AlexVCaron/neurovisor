from collections.abc import MutableMapping
from typing import List
from . import Dataflow
from .internals import Map


class Input(Dataflow):
    pass


class InputMap(Map):
    def __init__(
        self,
        names : List[str],
        inputs : List[Input],
        initializer : MutableMapping[str, Input] | None = None
    ):
        super().__init__(names, inputs, initializer)
