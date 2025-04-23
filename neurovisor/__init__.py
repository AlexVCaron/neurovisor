import itertools
import os
import tempfile


_XDG_CACHE_LOCATIONS = filter(lambda loc: loc is not None,[
    os.environ.get("XDG_CACHE_HOME", None),
    os.environ.get("XDG_DATA_HOME", None)
] + os.environ.get("XDG_DATA_DIRS", []))

_CACHE_LOCATIONS = filter(lambda loc: loc is not None, itertools.chain(
    _XDG_CACHE_LOCATIONS,
    [os.environ.get("NEUROVISOR_CACHE_LOCATION", None),
     tempfile.gettempdir()]))

CACHE_LOCATION = next(_CACHE_LOCATIONS, None)
