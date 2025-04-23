from neurovisor.driver.nextflow.parser import NextflowParser


def test_module_parsing(shared_datadir):
    module = NextflowParser.parse_module(f"{shared_datadir}/module/preproc/eddy")
    assert module["name"] == "PREPROC_EDDY"


def test_subworkflow_parsing(shared_datadir):
    sbwf = NextflowParser.parse_subworkflow(
        f"{shared_datadir}/subworkflow/preproc_dwi")
    assert sbwf["name"] == "PREPROC_DWI"
