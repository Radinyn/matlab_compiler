class Memory:

    def __init__(self, name):
        self.name = name
        self.lookup = {}
    
    def has_key(self, name):
        return name in self.lookup.keys()

    def get(self, name):
        if self.has_key(name):
            return self.lookup[name]
        raise None

    def put(self, name, value):
        # Here overrides are allowed in contrast to the symbol table
        self.lookup[name] = value

# Tbh we're forced to use this. 
# I structured the symbol table also as a stack for the purpouses of name-shadowings
class MemoryStack:
                                                                             
    def __init__(self, initial_memory=None):
        self.stack = [initial_memory]

    def get(self, name):       
        memory = next((mem for mem in self.stack[::-1] if mem.has_key(name)), None) 
        if memory is None:
            return None
        return memory.get(name)

    def insert(self, name, value):
        memory = next((mem for mem in self.stack[::-1] if mem.has_key(name)), None) 
        if memory is None:
            self.stack[-1].put(name, value)
        else:
            memory.put(name, value)

    def push(self, memory):
        self.stack.append(memory)

    def pop(self):
        return self.stack.pop()
    
    def dump_memory(self):
        for mem in self.stack:
            print(mem.name, mem.lookup)