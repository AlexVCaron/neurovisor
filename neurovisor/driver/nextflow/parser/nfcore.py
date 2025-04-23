from os import PathLike
from pathlib import Path
from nf_core.modules.lint import read_meta_yml
from nf_core.components.nfcore_component import NFCoreComponent

from neurovisor.backend import CacheManager


def load_meta_yml(component_name: str, component_dir: PathLike):
    component = NFCoreComponent(
        component_name,
        component_dir=component_dir,
        base_dir=CacheManager.get_nfcore_directory(),
        component_type=Path(component_dir).parent.parent,
        remote_component=False)
    return read_meta_yml(None, component)
