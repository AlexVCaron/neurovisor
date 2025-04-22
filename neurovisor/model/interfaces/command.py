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
        container : Container
    ):
        super().__init__(command)
        self.container = container

    def serialize(self):
        return {
            **super().serialize(),
            **{"container": self.container}
        }
