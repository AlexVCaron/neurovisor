from . import InputMap, OutputMap, StepMap, ParameterMap


class Workflow:
    def __init__(
        self,
        inputs : InputMap,
        outputs : OutputMap,
        steps : StepMap,
        config : ParameterMap
    ):
        self.inputs = inputs
        self.outputs = outputs
        self.steps = steps
        self.config = config
