from threading import Lock
from common.utils import Utils

DEFAULT_BUCKET_SIZE = 3145739  # 2 ^ 21 to 2 ^ 22


class SyncMap(object):
    def __init__(self, bucket_count=DEFAULT_BUCKET_SIZE, fn=None):
        self.bucket_count = bucket_count
        if fn is None:
            self.fn = lambda k: Utils.get_md5_based_hash_table_key(k)
        else:
            self.fn = fn
        self.map = {}

    def put(self, k, v):
        hash = self.fn(k) % self.bucket_count
        hash_val = self.map.get(hash)
        if hash_val is None:
            hash_val = (Lock(), {})
            self.map[hash] = hash_val
        lock, inner_map = hash_val
        with lock:
            inner_map[k] = v

    def get(self, k):
        hash = self.fn(k) % self.bucket_count
        hash_val = self.map.get(hash)
        if hash_val is None:
            return None
        lock, inner_map = hash_val
        with lock:
            return inner_map.get(k)

    def remove(self, k):
        hash = self.fn(k) % self.bucket_count
        hash_val = self.map.get(hash)
        if hash_val is None:
            return None
        lock, inner_map = hash_val
        with lock:
            v = inner_map[k]
            del inner_map[k]
            return v
