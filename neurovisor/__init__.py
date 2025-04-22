import os


_XDG_CACHE_LOCATIONS = [
    os.environ.get("XDG_CACHE_HOME", None),
    os.environ.get("XDG_DATA_HOME", None)
] + os.environ.get("XDG_DATA_DIRS", [])

_CACHE_LOCATIONS = [
    os.environ.get("NEUROVISOR_CACHE_LOCATION", None)
] + [
    os.path.join(d, "neurovisor") for d in
    filter(lambda a: a is not None, _XDG_CACHE_LOCATIONS)
]

CACHE_LOCATION = _CACHE_LOCATIONS.pop(0)
