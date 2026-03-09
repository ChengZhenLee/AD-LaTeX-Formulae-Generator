from src.notation.variable import Variable


class Monomial:
    """
    A class representing a monomial as a product of variables.
    A monomial is a mathematical expression consisting of a single term that is 
    a product of variables, each potentially raised to a power.

    Attributes:
        variables (list[Variable]): A list of Variable objects that make up the monomial.

    Methods:
        __init__(variables: list[Variable]) -> None:
            Initializes a Monomial with the given list of variables.

            Args:
                variables (list[Variable]): A list of Variable objects to be multiplied together.


        __str__() -> str:
            Returns a string representation of the monomial.

            Returns:
                str: A LaTeX-formatted string representation of the monomial with variables
                     separated by the multiplication symbol (\\cdot). Returns an empty string
                     if the monomial contains no variables.
    """
    
    def __init__(self, variables:list[Variable]):
        self.variables = variables

    
    def __str__(self)->str:
        variableStr:str = "\\cdot ".join([str(v) for v in self.variables])

        return variableStr if variableStr else ""