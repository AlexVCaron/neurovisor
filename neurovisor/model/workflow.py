from . import InputMap, OutputMap, StepMap, ParameterMap
from . import Step


class Workflow(Step):
    def __init__(
        self,
        inputs : InputMap,
        outputs : OutputMap,
        steps : StepMap,
        config : ParameterMap
    ):
        super().__init__(inputs, outputs, config)
        self.steps = steps

    def serialize(self):
        return {
            **super().serialize(),
            **{
                "steps": self.steps
            }
        }
