from . import Input, Output


class Channel:
    def __init__(
        self,
        input : Input,
        output : Output
    ):
        self.input = input
        self.output = output
