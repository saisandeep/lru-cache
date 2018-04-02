from threading import Lock
from common.db import DB
from lru_metadata import LruMeta
from lru_sync_map import SyncMap


class LRU(object):
    def __init__(self, max_size):
        self.lru_meta = LruMeta(max_size)
        self.meta_data_lock = Lock()
        self.cache = SyncMap()
        self.db = DB()

    def put(self, k, v):
        with self.meta_data_lock:
            evicted_key = None
            existing_value = self.cache.get(k)
            if existing_value is None:
                evicted_key = self.lru_meta.insert_key(k)
            else:
                self.lru_meta.refresh_key(k)
            self.cache.put(k, v)
            if evicted_key is not None:
                self.cache.remove(evicted_key)
            return evicted_key

    def get(self, k):
        with self.meta_data_lock:
            v = self.cache.get(k)
            if v is None:
                v = self.db.get(k)
                self.cache.put(k, v)
                self.lru_meta.insert_key(k)
            else:
                self.lru_meta.refresh_key(k)
            return v
