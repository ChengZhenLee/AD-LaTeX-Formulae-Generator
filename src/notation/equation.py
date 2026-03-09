from src.notation.monomial import Monomial
from src.notation.variable import Variable
from src.constants import ORDER_COLORS


class Equation:
    """
    Represents a mathematical equation with a left-hand side variable and right-hand side monomials.
    This class stores and formats equations for display, with support for color-coding based on
    the equation's order.

    Attributes:
        left (Variable): The left-hand side variable of the equation.
        right (list[Monomial]): List of monomials comprising the right-hand side of the equation.
        order (str): The order of the equation (default: "1"). Used to determine the color
                     for LaTeX rendering via ORDER_COLORS mapping.

    Methods:
        __str__() -> str:
            Returns a LaTeX-formatted string representation of the equation with color-coding
            based on the equation's order. The left-hand side is separated from the right-hand side
            with an equality symbol ('='). Each right-hand side term is separated by a plus symbol ('+')
            and are aligned vertically. Returns "0" if the right-hand side is empty.
    """
    def __init__(self, left:Variable, right:list[Monomial], order:str="1"):
        self.left = left
        self.right = right
        self.order = order
        

    def __str__(self)->str:
        leftStr:str = str(self.left)

        color:str = ORDER_COLORS.get(self.order, "Black")

        rightStr:str = f" \\\\ & \\color{{{color}}} \\: + ".join(str(m) for m in self.right) if self.right else "0"

        return f"\\color{{{color}}}{{{leftStr}}} & \\color{{{color}}}{{=}} \\ {rightStr}"