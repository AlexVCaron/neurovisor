from collections.abc import MutableMapping
from typing import List
from . import Dataflow
from .internals import Map


class Input(Dataflow):
    def __init__(self, spec, data=None):
        self.spec = spec
        super().__init__(data)

    def serialize(self):
        return {
            **super().serialize(),
            **{"spec": self.spec}
        }


class InputMap(Map):
    def __init__(
        self,
        names : List[str],
        inputs : List[Input],
        initializer : MutableMapping[str, Input] | None = None
    ):
        super().__init__(names, inputs, initializer)
