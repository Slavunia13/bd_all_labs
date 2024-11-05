from functools import lru_cache

from .default import DefaultSettings


@lru_cache
def getSettings() -> DefaultSettings:
    return DefaultSettings()
