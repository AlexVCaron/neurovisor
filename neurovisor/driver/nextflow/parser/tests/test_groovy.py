import json

from neurovisor.driver.nextflow.parser.groovy import unpack_nf_component


def test_unpack_nf_module(shared_datadir):
    with open(f"{shared_datadir}/module.json") as f:
        module = json.load(f)

    unpack_nf_component(module)


def test_unpack_nf_workflow(shared_datadir):
    with open(f"{shared_datadir}/workflow.json") as f:
        workflow = json.load(f)

    unpack_nf_component(workflow)
