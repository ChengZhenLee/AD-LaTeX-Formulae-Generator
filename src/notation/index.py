from __future__ import annotations


class Index():
    def __init__(self, name:str, num:str):
        self.name = name
        self.num = num

    
    def __eq__(self, other:object)->bool:  
        if not isinstance(other, Index):
            return False
              
        return self.name == other.name and self.num == other.num