from term import Term
from variable import Variable


class Equation:
    def __init__(self, left:Variable, right:list[Term]):
        self.left = left
        self.right = right