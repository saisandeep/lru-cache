import pytest
from v0.lru import LRU


@pytest.mark.gen_test
def test_1():
    cache = LRU(10)
    assert cache.get(2) == 1
    assert cache.cache == {2: 1}
    assert cache.lru_meta.order_head.get_vals() == [2]


@pytest.mark.gen_test
def test_2():
    cache = LRU(10)
    cache.put(2, 20)
    assert cache.get(2) == 20
    assert cache.cache == {2: 20}
    assert cache.lru_meta.order_head.get_vals() == [2]


@pytest.mark.gen_test
def test_3():
    cache = LRU(10)
    cache.put(2, 20)
    cache.put(2, 30)
    assert cache.get(2) == 30
    assert cache.cache == {2: 30}
    assert cache.lru_meta.order_head.get_vals() == [2]


@pytest.mark.gen_test
def test_4():
    cache = LRU(1)
    cache.put(2, 20)
    assert cache.cache == {2: 20}
    assert cache.lru_meta.order_head.get_vals() == [2]
    evicted_key = cache.put(4, 30)
    assert evicted_key == 2
    assert cache.get(4) == 30
    assert cache.cache == {4: 30}
    assert cache.lru_meta.order_head.get_vals() == [4]


@pytest.mark.gen_test
def test_5():
    cache = LRU(10)
    cache.put(1, 10)
    cache.put(2, 20)
    cache.put(3, 30)
    cache.put(4, 40)
    cache.put(5, 50)
    assert cache.lru_meta.order_head.get_vals() == [5, 4, 3, 2, 1]
    assert cache.get(4) == 40
    assert cache.lru_meta.order_head.get_vals() == [4, 5, 3, 2, 1]
    assert cache.get(3) == 30
    assert cache.lru_meta.order_head.get_vals() == [3, 4, 5, 2, 1]
    assert cache.get(1) == 10
    assert cache.lru_meta.order_head.get_vals() == [1, 3, 4, 5, 2]
    assert cache.put(6, 60) is None
    assert cache.lru_meta.order_head.get_vals() == [6, 1, 3, 4, 5, 2]
    assert cache.cache == {1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 60}
    assert cache.put(3, 300) is None
    assert cache.lru_meta.order_head.get_vals() == [3, 6, 1, 4, 5, 2]
    assert cache.cache == {1: 10, 2: 20, 3: 300, 4: 40, 5: 50, 6: 60}
