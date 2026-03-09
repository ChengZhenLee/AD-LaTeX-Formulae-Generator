from term import Term
from variable import Variable
from constants import ORDER_COLORS


class Equation:
    def __init__(self, left:Variable, right:list[Term], order:str="0"):
        self.left = left
        self.right = right
        self.order = order
        

    def __str__(self)->str:
        leftStr:str = str(self.left)

        rightStr:str = " + ".join(str(t) for t in self.right)
        rightStr = rightStr if rightStr else "0"

        equationStr:str = leftStr + " = " + rightStr
        color = ORDER_COLORS.get(self.order, "black")

        return f"\\color{{{color}}}{{{equationStr}}}"