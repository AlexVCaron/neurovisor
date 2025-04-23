from collections.abc import MutableMapping
from typing import List
from . import Dataflow
from .internals import Map


class Output(Dataflow):
    def __init__(self, spec, optional=False, data=None):
        self.spec = spec
        self.optional = optional
        super().__init__(data)

    def serialize(self):
        return {
            **super().serialize(),
            **{"spec": self.spec, "optional": self.optional}
        }


class OutputMap(Map):
    def __init__(
        self,
        names : List[str] | None = None,
        outputs : List[Output] | None = None,
        initializer : MutableMapping[str, Output] | None = None
    ):
        super().__init__(names, outputs, initializer)
