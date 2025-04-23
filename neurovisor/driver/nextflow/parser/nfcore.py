from os import PathLike
from pathlib import Path
from nf_core.modules.lint import read_meta_yml
from nf_core.components.nfcore_component import NFCoreComponent

from neurovisor.backend import CacheManager


def load_meta_yml(component_name: str, component_dir: PathLike):
    component = NFCoreComponent(
        component_name,
        component_dir=Path(component_dir),
        base_dir=Path(CacheManager.get_nfcore_directory()),
        component_type=Path(component_dir).parent.parent.name,
        remote_component=False,
        repo_url="www.dummy.boy",
        repo_type="modules")
    return read_meta_yml(None, component)
