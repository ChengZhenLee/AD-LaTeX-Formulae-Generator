from __future__ import annotations
from .index import Index
import src.constants as constants


class Variable:
    """
    Variable class represents a mathematical variable with indices, subscripts, and superscripts.
    This class is used to represent variables in automatic differentiation notation, supporting
    tangent and adjoint modes with associated indices and order information.

    Attributes:
        name (str): The base name of the variable (e.g., 'X', 'Y').
        indices (list[Index]): List of Index objects representing the variable's indices (e.g. 'i_2', 'j').
        sub (list[str]): List of subscript labels for adjoint derivatives (e.g. (1, 2)).
        sup (list[str]): List of superscript labels for tangent derivatives (e.g. (1, 3)).
        order (str): The derivation order, default is '1'.

    Methods:
        derive(mode: str = "", order: str = "1") -> Variable:
            Creates a new Variable with applied derivatives in the specified mode.

            Args:
                mode (str): The derivation mode - either TANGENT or ADJOINT mode constant.
                order (str): The order of derivation to append.

            Returns:
                Variable: A new Variable instance with updated indices, subscripts, and superscripts.

                
        isEqual(v1: Variable, v2: Variable) -> bool:
            Static method that compares two variables for equality.

            Args:
                v1 (Variable): First variable to compare.
                v2 (Variable): Second variable to compare.

            Returns:
                bool: True if all attributes match, False otherwise.

                
        __str__() -> str:
            Returns the LaTeX-formatted string representation of the variable.

            Returns:
                str: LaTeX formatted string with base name, adjoint part, indices, and tangent part.
    """

    def __init__(self, name:str, indices:list[Index], sub:list[str]=[], sup:list[str]=[], order:str='1'):
        self.name = name
        self.sub = sub
        self.sup = sup
        self.indices = indices
        self.order = order
    

    def derive(self, mode:str="", order:str="1")->Variable:
        newIndices = self.indices.copy()
        newSub = self.sub.copy()
        newSup = self.sup.copy()

        if mode == constants.TANGENT:
            newSup.append(order)
            newIndices.append(Index(constants.NU, order))
        elif mode == constants.ADJOINT:
            newSub.append(order)
            newIndices = [Index(constants.MU, order)] + newIndices
        
        return Variable(self.name, newIndices, newSub, newSup, order)
    

    @staticmethod
    def isEqual(v1:Variable, v2:Variable):
        return (
            v1.name == v2.name and
            v1.indices == v2.indices and
            v1.sub == v2.sub and
            v1.sup == v2.sup and 
            v1.order == v2.order
        )
    

    def __str__(self)->str:
        # Collect the name of the variable
        nameStr:str = self.name

        # Collect the tangent part of the variable
        supContent:str = ",".join(self.sup)
        tangentStr:str = f"({supContent})" if supContent else ""

        # Collect the adjoint part of the variable
        subContent:str = ",".join(self.sub)
        adjointStr:str = f"({subContent}) " if subContent else ""

        # Collect the indices of the variable
        indexParts:list[str] = []
        for index in self.indices:
            indexParts += [f"{index.name}_{{{index.num}}}"] if index.num != '0' else [f"{index.name}"]
        indicesStr:str = ",".join(indexParts) if indexParts else ""


        return nameStr + "_{" + adjointStr + indicesStr + "}^{" + tangentStr + "}"



class X(Variable):
    """
    Initialize a variable X with specified mode and order.

    Args:
        mode (str): The mode of the variable. Supported modes are:
            - constants.TANGENT: Adds order to superscripts and includes a nu index
            - constants.ADJOINT: Adds order to subscripts and prepends a mu index
        order (str, optional): The order of the variable. Defaults to '1'.

    Attributes:
        name (str): The variable name (inherited from Variable, set to constants.X)
        order (str): The highest index order (default: '1')
        indices (list[Index]): List of indices for the variable, starting with Index('i', order).
            - For TANGENT mode: includes an additional Index(constants.NU, order)
            - For ADJOINT mode: prepended with Index(constants.MU, order)
        sub (list[str]): List of subscripts. For ADJOINT mode, contains the order value.
        sup (list[str]): List of superscripts. For TANGENT mode, contains the order value.
    """

    def __init__(self, mode:str, order:str='1'):
        indices:list[Index] = [Index('i', order)]
        sub:list[str] = []
        sup:list[str] = []

        if mode == constants.TANGENT:
            sup.append(order)
            indices += [Index(constants.NU, order)]
        elif mode == constants.ADJOINT:
            sub.append(order)
            indices = [Index(constants.MU, order)] + indices

        super().__init__(constants.X, indices, sub, sup, order)


class Y(Variable):
    """
    Initialize a variable Y with specified mode and order.

    Args:
        mode (str): The mode of the variable. Supported modes are:
            - constants.TANGENT: Adds order to superscripts and includes a nu index
            - constants.ADJOINT: Adds order to subscripts and prepends a mu index
        order (str, optional): The order of the variable. Defaults to '1'.

    Attributes:
        name (str): The variable name (inherited from Variable, set to constants.Y)
        order (str): The highest index order (default: '1')
        indices (list[Index]): List of indices for the variable, starting with Index('j', '0').
            - For TANGENT mode: includes an additional Index(constants.NU, order)
            - For ADJOINT mode: prepended with Index(constants.MU, order)
        sub (list[str]): List of subscripts. For ADJOINT mode, contains the order value.
        sup (list[str]): List of superscripts. For TANGENT mode, contains the order value.
    """

    def __init__(self, mode:str, order:str='1'):
        indices:list[Index] = [Index('j', '0')]
        sub:list[str] = []
        sup:list[str] = []

        if mode == constants.TANGENT:
            sup.append(order)
            indices += [Index(constants.NU, order)]
        elif mode == constants.ADJOINT:
            sub.append(order)
            indices = [Index(constants.MU, order)] + indices

        super().__init__(constants.Y, indices, sub, sup, order)


class F(Variable):
    """
    Represents a derived variable F with support for automatic differentiation.
    The F class extends Variable to manage a mathematical function F with:
        - Multiple indices that track dimensions and derivative orders
        - Derivative tracking through the `derived` attribute
        - Support for automatic differentiation via the `derive` method
        - LaTeX-formatted string representation

    Attributes:
        derived (str): The derivative order of this F variable (default: '1')
        name (str): The variable name (inherited from Variable, set to constants.F)
        order (str): The highest index order (default: '1')
        indices (list[Index]): List of Index objects representing dimensions (default: [Index('j', '0'), Index('i', order)])
        sub (list[str]): Subscripts (inherited from Variable, default: [])
        sup (list[str]): Superscripts (inherited from Variable, default: [])

    Methods:
        derive(mode: str = "", order: str = "1") -> F:
            Creates a new F variable with incremented derivative and order.

            Returns:
                F: A new F instance with derived incremented by 1, 
                   and an additional index appended


        __str__() -> str:
            Returns LaTeX-formatted representation of F with indices and derivative order.
            Format: F_{index_list}^{[derived_number]}
    """

    def __init__(self, order:str='1', indices:list[Index]=[], derived:str='1'):
        self.derived = derived
        if len(indices) == 0:
            indices = [Index('j', '0'), Index('i', order)]

        super().__init__(constants.F, indices, sub=[], sup=[], order=order) 

    
    def derive(self, mode:str="", order:str="1")->F:
        newDerived = str(int(self.derived) + 1)

        newIndices = self.indices + [Index('i', order)]

        return F(order=order, indices=newIndices, derived=newDerived)
    

    def __str__(self)->str:
        nameStr:str = self.name

        # Get the derived number of F
        derivedStr:str = f"[{self.derived}]"

        # Get the indices of F
        indexParts:list[str] = []
        for index in self.indices:
            indexParts += [f"{index.name}_{{{index.num}}}"] if index.num != '0' else [f"{index.name}"]
        indicesStr:str = ",".join(indexParts) if indexParts else ""

        return nameStr + "_{" + indicesStr + "}^{" + derivedStr + "}"
