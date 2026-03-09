from term import Term
from variable import Variable


class Equation:
    def __init__(self, left:Variable, right:list[Term]):
        self.left = left
        self.right = right
        

    def __str__(self)->str:
        leftStr:str = str(self.left)

        rightStr:str = " + ".join(str(t) for t in self.right)
        rightStr = rightStr if rightStr else "0"

        return leftStr + " = " + rightStr 