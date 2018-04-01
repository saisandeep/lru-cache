class DLL(object):
    def __init__(self, k):
        self.k = k
        self.next = None
        self.prev = None

    @staticmethod
    def print_nexts(node):
        while node is not None:
            print node.k
            node = node.next

    @staticmethod
    def print_prevs(node):
        while node is not None:
            print node.k
            node = node.prev

    def get_vals(self, head_sentinel=True, tail_sentinel=True):
        list = []
        node = self
        while node is not None:
            list.append(node.k)
            node = node.next
        if head_sentinel:
            list = list[1:]
        if tail_sentinel:
            list = list[:-1]
        return list


class LruMeta(object):
    def __init__(self, max_size):
        start_sentinel = DLL(0)
        end_sentinel = DLL(0)
        start_sentinel.next = end_sentinel
        end_sentinel.prev = start_sentinel
        self.size = 0
        self.MAX_SIZE = max_size
        self.order_head = start_sentinel  # recent
        self.order_tail = end_sentinel  # to be evicted
        self.order_lookup = {}

    def _insert_front(self, node):
        self.order_head.next.prev = node
        node.next = self.order_head.next
        self.order_head.next = node
        node.prev = self.order_head

    def refresh_key(self, k):
        if k not in self.order_lookup:
            raise Exception("Accessed Key not present in"
                            " the LRU order list: " + k)
        list_node = self.order_lookup.get(k)
        prev_node = list_node.prev
        next_node = list_node.next
        prev_node.next = next_node
        next_node.prev = prev_node
        self._insert_front(list_node)

    def insert_key(self, k):
        evicted_key = None
        if self.size == self.MAX_SIZE:
            evicted_key = self._evict()
        self.size += 1
        node = DLL(k)
        self._insert_front(node)
        self.order_lookup[k] = node
        return evicted_key

    def _evict(self):
        node_to_be_evicted = self.order_tail.prev
        self.order_tail.prev.prev.next = self.order_tail
        self.order_tail.prev = self.order_tail.prev.prev
        del self.order_lookup[node_to_be_evicted.k]
        self.size -= 1
        return node_to_be_evicted.k
