from typing import List
from . import Module, Channel, Configuration


class Pipeline:
    def __init__(
        self,
        steps : List[Module],
        channels : List[Channel],
        config : Configuration
    ):
        # Steps become nodes if not workflow, else become subnetworks
        # Channels become links
        # Config form sub-networks with steps nodes
        # Config augment workflows sub-networks
        self.steps = steps
        self.channels = channels
        self.config = config
