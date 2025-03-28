from typing import List
from collections.abc import MutableMapping
from . import InputMap, OutputMap, ParameterMap
from internals import Map


class Step:
    def __init__(
        self,
        inputs : InputMap,
        outputs : OutputMap,
        parameters : ParameterMap
    ):
        self.inputs = inputs
        self.outputs = outputs
        self.parameters = parameters


class StepMap(Map):
    def __init__(
        self,
        names : List[str],
        steps : List[Step],
        initializer : MutableMapping[str, Step] | None = None
    ):
        super().__init__(names, steps, initializer)
