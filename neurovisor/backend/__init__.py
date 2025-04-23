from os.path import join

from neurovisor import CACHE_LOCATION


class CacheManager:
    @classmethod
    def get_cache_directory(cls):
        return CACHE_LOCATION

    @classmethod
    def get_nfcore_directory(cls):
        return join(CacheManager.get_cache_directory(), "nfcore")
