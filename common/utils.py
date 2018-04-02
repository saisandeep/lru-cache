import hashlib


class Utils(object):
    @staticmethod
    def get_md5_hash_upto_a_position(k, size=10):
        m = hashlib.md5()
        m.update(str(k))
        return m.hexdigest()[:size]

    @staticmethod
    def get_md5_based_hash_table_key(k):
        md5_hash_key = Utils.get_md5_hash_upto_a_position(k)
        return int(md5_hash_key, 16)

