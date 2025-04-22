from typing import List

from .internals import Serializable


class Data(Serializable):
    pass


class Dataflow(Serializable):
    def __init__(
        self,
        data : List[Data]
    ):
        self.data = data

    def serialize(self):
        return {
            "type": type(self),
            "data": self.data
        }