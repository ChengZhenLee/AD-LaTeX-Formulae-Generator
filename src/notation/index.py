from __future__ import annotations


class Index():
    """
    A class representing an index with a name and number.

    Attributes:
        name (str): The name of the index.
        num (str): The number associated with the index.

    Methods:
        __eq__(other: object) -> bool: Compares two Index objects for equality based on their name and num attributes.
    """
    def __init__(self, name:str, num:str):
        self.name = name
        self.num = num

    
    def __eq__(self, other:object)->bool:  
        if not isinstance(other, Index):
            return False
              
        return self.name == other.name and self.num == other.num