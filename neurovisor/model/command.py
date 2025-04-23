from .internals import Serializable
from . import Container


class Command(Serializable):
    def __init__(
        self,
        command : str
    ):
        self.command = command

    def serialize(self):
        return {
            "command": self.command
        }



class ContainerCommand(Command):
    def __init__(
        self,
        command : str,
        containers : list[Container]
    ):
        super().__init__(command)
        self.containers = containers

    def serialize(self):
        return {
            **super().serialize(),
            **{"containers": [c.serialize() for c in self.containers]}
        }
