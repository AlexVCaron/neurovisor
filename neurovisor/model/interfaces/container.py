from .internals import Serializable
from . import ParameterMap


class Image(Serializable):
    pass


class Container(Serializable):
    def __init__(
        self,
        image : Image,
        configuration : ParameterMap
    ):
        self.image = image
        self.configuration = configuration

    def serialize(self):
        return {
            "image": self.image,
            "configuration": self.configuration
        }
