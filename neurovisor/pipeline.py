from typing import List
from .model import Step, Subworkflow, Channel, Configuration


class Pipeline:
    def __init__(
        self,
        steps : List[Step],
        workflows : List[Subworkflow],
        channels : List[Channel],
        config : Configuration
    ):
        # Steps become nodes
        # Channels become links
        # Workflows become sub-networks
        # Config form sub-networks with steps nodes
        # Config augment workflows sub-networks
        self.steps = steps
        self.workflows = workflows
        self.channels = channels
        self.config = config
