from .internals import Serializable
from . import Input, Output


class Channel(Serializable):
    def __init__(
        self,
        input : Input,
        output : Output
    ):
        self.input = input
        self.output = output

    def serialize(self):
        return {
            "input": self.input,
            "output": self.output
        }
