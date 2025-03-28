from collections import OrderedDict
from bamt.nodes.gaussian_node import GaussianNode
from bamt.nodes.discrete_node import DiscreteNode
from bamt.nodes.conditional_gaussian_node import ConditionalGaussianNode

from ..model.interfaces import (
    Data, Parameter, ParameterMap
)


class DEFAULT_NODE_TYPES(OrderedDict):
    def __init__(self):
        super().__init__({
            Data: GaussianNode,
            Parameter: DiscreteNode,
            ParameterMap: ConditionalGaussianNode
        })
