from threading import Lock
from common.db import DB
from lru_metadata import LruMeta


class LRU(object):
    def __init__(self, max_size):
        self.lru_meta = LruMeta(max_size)
        self.cache = {}
        self.cache_lock = Lock()
        self.db = DB()

    def put(self, k, v):
        with self.cache_lock:
            evicted_key = None
            existing_value = self.cache.get(k)
            if existing_value is None:
                evicted_key = self.lru_meta.insert_key(k)
            else:
                self.lru_meta.refresh_key(k)
            self.cache[k] = v
            if evicted_key is not None:
                del self.cache[evicted_key]
            return evicted_key

    def get(self, k):
        with self.cache_lock:
            v = self.cache.get(k)
            if v is None:
                v = self.db.get(k)
                self.cache[k] = v
                self.lru_meta.insert_key(k)
            else:
                self.lru_meta.refresh_key(k)
            return v
