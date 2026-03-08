from index import Index


class Variable:
    def __init__(self, name:str, indices:list[Index], sub:list[str]=[], sup:list[str]=[]):
        self.name = name
        self.sub = sub
        self.sup = sup
        self.indices = indices