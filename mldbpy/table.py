import re

from typing import List, Any, Dict, Hashable, Tuple, Union, Callable, Iterable

from rich import print
from rich.table import Table

from mldbpy.exceptions import (
    IllegalEntryError,
    MissingAttributeError,
    IllegalKeyFunctionError,
    DuplicateEntryError,
    AttributeDomainError,
)


class Attribute:
    def __init__(self, name: str, domain: Union[None, str, Callable] = None):
        self.__name = name.upper()

        if domain is None:
            self.__validator = lambda _: True
        elif type(domain) is str:
            self.__validator = lambda v: re.compile(domain).match(str(v))
        else:
            self.__validator = domain

    def validate(self, entry: Any) -> Any:
        if not self.__validator(entry):
            raise AttributeDomainError

        return entry

    @property
    def name(self):
        return self.__name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name


class Relation:
    def __init__(
        self,
        attributes: List[Union[str, Attribute]],
        key: Union[str, List[str]] = None,
    ):
        self.__attributes: List[Attribute] = []
        self.__entries: Dict[int, Tuple[Hashable]] = {}
        self.__attribute_indeces: Dict[str, int] = {}

        i = 0
        for attrib in attributes:
            if type(attrib) is str:
                attrib = Attribute(attrib)

            self.__attributes.append(attrib)

            self.__attribute_indeces[attrib.name] = i
            i += 1

        ### Init key function
        if key is None:
            self.__key = lambda e: hash(e[0])

        elif isinstance(key, str):
            if not key in self.__attribute_indeces.keys():
                raise IllegalKeyFunctionError

            self.__key = lambda e: hash(e[self.__attribute_indeces[key]])

        elif isinstance(key, list):
            keys = [key]
            if not set(keys).issubset(self.__attribute_indeces.keys()):
                raise IllegalKeyFunctionError

            self.__key = lambda e: hash(tuple(e[self.__attribute_indeces[k]] for k in keys))

    def print(self):
        t = Table(*[a.name for a in self.__attributes])
        for e in self.__entries.values():
            t.add_row(*(str(i) for i in e))

        print(t)

    def domain(self, attribute: str) -> List[Any]:
        return 

    def add_entry(self, val: Iterable[Hashable]):
        attrib_count = len(val)

        if attrib_count != len(self.__attributes):
            raise IllegalEntryError

        k = self.__key(val)

        if k in self.__entries:
            raise DuplicateEntryError

        self.__entries[k] = tuple(attrib.validate(e) for attrib, e in zip(self.__attributes, val))

    def index_of(self, attrib: Union[str, Attribute]) -> int:
        if str(attrib) in self.__attributes:
            return self.__attribute_indeces[str(attrib)]
        else:
            raise MissingAttributeError
