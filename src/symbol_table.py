from dataclasses import dataclass
from typing import Tuple

@dataclass(eq=False)
class Symbol():
    # This might not be necessary since the SymbolTable holds all the names
    type: str
    shape: Tuple[int, ...]

    def __eq__(self, other):
        return self is not None and other is not None and self.type == other.type and self.shape == other.shape

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
        node = self
        while node is not None:
            if name in node.lookup.keys():
                return node.lookup[name]
            node = node.parent_context
        return None 

    def push_context(self, name):
        return SymbolTable(self, name)

    def pop_context(self):
        return self.parent_context
    
    def is_looping(self):
        node = self
        while node is not None:
            if node.name in ["for", "while"]:
                return True
            node = node.parent_context
        return False