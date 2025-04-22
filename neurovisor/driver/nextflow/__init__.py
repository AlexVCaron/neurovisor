from os import PathLike
from .parsing import NextflowParser
from ...model import (
    Module as _Module,
    Subworkflow as _Subworkflow,
    Pipeline as _Pipeline,
    Configuration as _Configuration
)


class Module(_Module):
    def __init__(self, filename : PathLike):
        module_from_groovy = NextflowParser.parse_module(filename)
        # - Get metadata as well
        #     meta = NextflowParse.nfcore.parse_meta(f"{dirname(filename)}/meta.yml")
        #   - May thrown an error if meta.yml doesn't exist
        # - Merge meta and module_from_groovy
        #     module = hierarcal_merge(module_from_groovy, meta)
        # - Supply that to super(), either we use **kwargs or upack from dict()
        #     super().__init__(**module)



class Subworkflow(_Subworkflow):
    def __init__(self, filename : PathLike):
        # see module comment
        sbwf_from_groovy = NextflowParser.parse_module(filename)
        pass


class Pipeline(_Pipeline):
    def __init__(self, filename : PathLike):
        # see module comment
        raise NotImplementedError()


class Configuration(_Configuration):
    def __init__(self, filename : PathLike):
        # see module comment
        raise NotImplementedError()
