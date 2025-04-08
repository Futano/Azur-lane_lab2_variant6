from typing import Optional, Callable, TypeVar, Generic, List, Tuple, Iterator

KT = TypeVar("KT")
VT = TypeVar("VT")
AccT = TypeVar("AccT")


class ImmutableDict(Generic[KT, VT]):
    def __init__(self, items: Optional[List[Tuple[KT, VT]]] = None):

        if items is None:
            self._items: List[Tuple[KT, VT]] = []
        else:
            temp = {}
            for k, v in items:
                temp[k] = v
            self._items = sorted(temp.items(), key=lambda x: x[0])

    def add(self, key: KT, value: VT) -> "ImmutableDict[KT, VT]":
        """返回新字典，包含更新项"""
        return ImmutableDict([(k, v) for k, v in self._items if k != key] + [(key, value)])

    def remove(self, key: KT) -> "ImmutableDict[KT, VT]":
        """返回新字典，不包含指定项"""
        return ImmutableDict([(k, v) for k, v in self._items if k != key])

    def search(self, key: KT) -> Optional[VT]:
        """递归查找值"""
        def _search(items):
            if not items:
                return None
            k, v = items[0]
            return v if k == key else _search(items[1:])
        return _search(self._items)

    def member(self, value: VT) -> bool:
        """是否包含值"""
        def _check(items):
            if not items:
                return False
            _, v = items[0]
            return v == value or _check(items[1:])
        return _check(self._items)

    def size(self) -> int:
        return len(self._items)

    def to_list(self) -> List[Tuple[KT, VT]]:
        return list(self._items)

    def map(self, func: Callable[[KT, VT], Tuple[KT, VT]]) -> "ImmutableDict[KT, VT]":
        return ImmutableDict([func(k, v) for k, v in self._items])

    def filter(self, predicate: Callable[[KT, VT], bool]) -> "ImmutableDict[KT, VT]":
        return ImmutableDict([(k, v) for k, v in self._items if predicate(k, v)])

    def reduce(self, func: Callable[[AccT, KT, VT], AccT], initial_value: AccT) -> AccT:
        def _reduce(items, acc):
            if not items:
                return acc
            k, v = items[0]
            return _reduce(items[1:], func(acc, k, v))
        return _reduce(self._items, initial_value)

    def concat(self, other: "ImmutableDict[KT, VT]") -> "ImmutableDict[KT, VT]":
        return ImmutableDict(self._items + other.to_list())

    def __iter__(self) -> Iterator[Tuple[KT, VT]]:
        return iter(self._items)

    @staticmethod
    def from_list(data: List[Tuple[KT, VT]]) -> "ImmutableDict[KT, VT]":
        return ImmutableDict(data)

    @staticmethod
    def empty() -> "ImmutableDict[KT, VT]":
        return ImmutableDict()
