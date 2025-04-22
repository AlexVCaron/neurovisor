from typing import List
from collections.abc import MutableMapping
from . import Command, InputMap, OutputMap, ParameterMap
from .internals import Map, Serializable


class Step(Serializable):
    def __init__(
        self,
        inputs : InputMap,
        outputs : OutputMap,
        parameters : ParameterMap,
        command : Command
    ):
        self.inputs = inputs
        self.outputs = outputs
        self.parameters = parameters
        self.command = command

    def serialize(self):
        return {
            "inputs": self.inputs,
            "outputs": self.outputs,
            "parameters": self.parameters,
            "command": self.command
        }


class StepMap(Map):
    def __init__(
        self,
        names : List[str],
        steps : List[Step],
        initializer : MutableMapping[str, Step] | None = None
    ):
        super().__init__(names, steps, initializer)
