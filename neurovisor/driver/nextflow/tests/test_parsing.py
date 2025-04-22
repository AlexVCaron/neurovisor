from neurovisor.driver.nextflow.parsing import NextflowParser


def test_module_parsing(shared_datadir):
    module = NextflowParser.parse_module(f"{shared_datadir}/module_eddy.nf")
