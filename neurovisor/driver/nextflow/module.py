from .parser import NextflowParser
from neurovisor.model import (
    Step as _Step,
    ContainerCommand,
    Container,
    Input,
    InputMap,
    Output,
    OutputMap,
    ParameterMap
)


def create_input_map(inputs: list[str]):
    # Inputs in nextflow are unnamed. They get assigned a number based on their
    # position in the input: definition.
    #
    # Parameters
    # ----------
    # inputs : list[str]
    #   list of input specs, e.g. "tuple val(meta),path(img)"
    # Returns
    # -------
    # input_map : InputMap
    #   map of numbered input fields
    return InputMap(initializer={
        i: Input(_spec) for i, _spec in enumerate(inputs)})


def create_output_map(outputs):
    # Outputs in nextflow are named. They get assigned a name based on the
    # output: definition emit field.
    #
    # Parameters
    # ----------
    # outputs : list[str]
    #   list of output specs, e.g. "tuple val(meta),path(img),emit:img".
    #   Optional fields are specified with "optional:true"
    # Returns
    # -------
    # output_map : OutputMap
    #   map of named output fields
    #   e.g. {"img": Output("tuple val(meta),path(img)")}
    def _unpack(output):
        _name, _out = None, {}
        _it = output.split(",")
        for _part in _it[::-1]:
            if "optional" in _part:
                _out["optional"] = "true" in _part.split(":")[1]
            elif "emit" in _part:
                _name = _part.split(":")[1].strip()
            else:
                _out["spec"] = _part.strip()
        return (_name, Output(**_out))

    return OutputMap(initializer=dict(_unpack(o) for o in outputs))


def create_parameters_map(args):
    return ParameterMap()


def create_container_command(script, containers):
    # Containers in nextflow are specified in the script field. They are
    # specified in the form of "container: containers_definition". The
    # definition can be a single name of a groovy closure doing a selection.
    #
    # Parameters
    # ----------
    # script : str
    #   script field of the module
    # containers : str
    #   containers field of the module
    # Returns
    # -------
    # container_command : ContainerCommand
    #   container command object
    #   e.g. ContainerCommand(script, [Container("container_name", ParameterMap())])
    if "?" in containers:
        containers = containers.split("?")[1]

    containers = containers.split("{")[-1].split("}")[0]

    if ":" in containers:
        containers = [c.strip() for c in containers.split(":")]
    else:
        containers = [containers.strip()]

    return ContainerCommand(
        script, [Container(c, ParameterMap()) for c in containers])


class Module(_Step):
    def __init__(self, filename: str):
        module = NextflowParser.parse_module(filename)
        super().__init__(
            create_input_map(module["inputs"]),
            create_output_map(module["outputs"]),
            create_parameters_map(module["args"]),
            create_container_command(module["script"], module["containers"]))
