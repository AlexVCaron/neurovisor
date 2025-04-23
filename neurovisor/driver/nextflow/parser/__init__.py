from os.path import join, split
from groovy_parser.parser import parse_and_digest_groovy_content

from neurovisor.backend import CacheManager
from .groovy import unpack_nf_component
from .nfcore import load_meta_yml


class NextflowParser:
    @classmethod
    def parse_module(cls, module_path : str):
        remainder, name = split(module_path)
        directory, remainder = split(remainder)
        return NextflowParser._parse_groovy(join(remainder, name), directory)

        # module = NFCoreComponent(
        #     "_".join(module_path.split("/")[-2:]).upper(),
        #     component_dir=module_path,
        #     base_dir="/".join(module_path.split("/")[:-2]),
        #     component_type="module",
        #     remote_component=False
        # )

        # # Split script from parameters
        # script = []
        # parameters = []
        # with open(module.main_nf, "r+") as f:
        #     while not "script:" in f.readline():
        #         continue
        #     line = f.readline()
        #     while not "\"\"\"" in line:
        #         # parse potential params, then append to script,
        #         # since parameter management is part of it
        #         line = f.readline()
        #         if "task.ext" in line:
        #             for match in re.match(".*task\.ext\.(\w+).*").groups():
        #                 if match not in parameters:
        #                     parameters.append(match)

        #         script.append(line)
            
        #     # remainder of the file can be thought as script
        #     script += f.readlines()
                
        # # Get container information

        # return {
        #     "inputs": module.get_inputs_from_main_nf(),
        #     "outputs": module.get_inputs_from_main_nf(),
        #     "parameters": parameters,
        #     "command": script
        # }


    @classmethod
    def parse_subworkflow(cls, subworkflow_path: str):
        directory, name = split(subworkflow_path)
        return NextflowParser._parse_groovy(directory, name)

    @classmethod
    def parse_configuration(cls, config_path: str):
        raise NotImplementedError()

    @classmethod
    def parse_pipeline(cls, pipeline_path: str):
        directory, name = split(pipeline_path)
        return NextflowParser._parse_groovy(directory, name, False)

    @classmethod
    def _parse_groovy(cls, name, directory, meta=True):
        with open(join(directory, name), "r") as f:
            json_tree = parse_and_digest_groovy_content(
                f.read(),
                CacheManager.get_cache_directory(),
                CacheManager.get_cache_directory())

            component = unpack_nf_component(json_tree)
            if meta:
                component["meta"] = load_meta_yml(name, directory)

            return component
