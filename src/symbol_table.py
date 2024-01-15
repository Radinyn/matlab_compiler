from dataclasses import dataclass
from typing import Tuple

@dataclass(eq=False)
class Symbol():
    # This might not be necessary since the SymbolTable holds all the names
    type: str
    shape: Tuple[int, ...]

    def __eq__(self, other):
        return self.type == other.type and self.shape == other.shape

class SymbolTable(object):

    def __init__(self, parent, name):
        self.parent_context = parent
        self.name = name
        self.lookup = {}

    def put(self, name, symbol):
        if not name in self.lookup.keys():
            self.lookup[name] = symbol
        else:
            # TODO: There are probably better ways of handling this 
            raise Exception("Trying to put a symbol that's already defined.")

    def get(self, name):
        if not name in self.lookup.keys():
            return None
        return self.lookup[name] 

    def get_parent_context(self):
        return self.parent_context

    def push_context(self, name):
        return SymbolTable(self, name)

    def pop_context(self):
        return self.parent_context
