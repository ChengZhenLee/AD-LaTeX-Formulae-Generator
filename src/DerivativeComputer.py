from copy import deepcopy
from src.notation.equation import Equation
from src.notation.monomial import Monomial
from src.notation.variable import Variable, X, Y, F
import src.constants as constants


class DerivativeComputer(): 

    @staticmethod
    def computeDerivative(modes:str, equations:list[Equation]=[])->list[Equation]:
        """
        Recursively computes derivative equations for a given sequence of differentiation modes.
        This method processes a string of differentiation modes (tangent or adjoint) and applies
        the corresponding derivative computations recursively. The recursion processes one mode
        at a time from left to right, building up the derivative equations with each iteration.

        Args:
            modes (str): A string of differentiation mode identifiers where each character represents
                        a mode to apply (e.g., 't' for tangent, 'a' for adjoint).
            equations (list[Equation], optional): The list of equations to differentiate. Defaults to
                                                an empty list. On the first call, this is typically
                                                the initial set of equations; on recursive calls,
                                                it contains previously computed derivatives.

        Returns:
            list[Equation]: A list of all equations including the original equations and all
                        computed derivative equations corresponding to the applied modes.
        """
        order = str(len(modes))

        # base case
        if order == '0':
            return equations
        
        # recursive
        mode = modes[0]
        rest = modes[1:]
        result = DerivativeComputer.computeDerivative(rest, equations)

        if mode == constants.TANGENT:
            result = DerivativeComputer._tangentMode(result, order)
        elif mode == constants.ADJOINT:
            result = DerivativeComputer._adjointMode(result, order)

        return result
        

    @staticmethod

    def _tangentMode(equations:list[Equation], order:str)->list[Equation]:
        """
        Compute tangent mode derivatives for a list of equations.
        This function performs tangent mode automatic differentiation on a system of equations.
        It derives each equation with respect to the tangent direction and generates new derivative
        equations. Additionally, it constructs a tangent output equation for output y.

        Args:
            equations (list[Equation]): A list of Equation objects representing the original system.
            order (str): The derivative order or tangent direction identifier.

        Returns:
            list[Equation]: A list of new equations containing:
                - The original equations
                - Derived versions of each original equation in tangent mode
                - An additional equation for the tangent output Y in terms of F and tangent X
        """
        result:list[Equation] = deepcopy(equations)

        # Perform tangent mode on the existing equations
        for equation in equations:
            newLeftVar:Variable = equation.left.derive(constants.TANGENT, order=order)
            newEquation:Equation = Equation(newLeftVar, [], order=order)
            
            for monomial in equation.right:
                # Perform product rule on each variable in the monomial
                for i, var in enumerate(monomial.variables):
                    newMonomial:Monomial = Monomial([])
                    newVar:Variable = var.derive(constants.TANGENT, order=order)

                    tempVar:list[Variable] = monomial.variables.copy()
                    tempVar.pop(i)

                    if var.name == constants.F:
                        # The function F should always be at the front
                        newMonomial.variables = [newVar]
                        newMonomial.variables += tempVar
                        newMonomial.variables.append(X(constants.TANGENT, order=order))
                    else:
                        newMonomial.variables = tempVar
                        newMonomial.variables.append(newVar)
                    
                    newEquation.right.append(newMonomial)

            result.append(newEquation)

        
        # Append the additional tangent "Y" equation
        newEquation:Equation = Equation(
            Y(constants.TANGENT, order=order),
            right=[Monomial([F(order=order), X(constants.TANGENT, order=order)])],
            order=order
        )
        result.append(newEquation)

        return result


    @staticmethod
    def _adjointMode(equations:list[Equation], order:str)->list[Equation]:
        """
        Computes the adjoint mode (reverse-mode automatic differentiation) for a system of equations.
        This function performs adjoint mode algorithmic differentiation on a set of equations. For each 
        unique input variable on the right-hand side of the equations, it generates a corresponding adjoint 
        equation. Additionally, it constructs an adjoint output equation for variable x.#

        Args:
            equations (list[Equation]): A list of Equation objects representing the forward computational graph.
                Each equation contains a left-hand side variable and right-hand side monomials (monomials).
            order (str): The differentiation order to apply to derived variables in the adjoint equations.

        Returns:
            list[Equation]: A new list of equations containing:
                - The original equations
                - One adjoint equation for each unique input variable found in the right-hand sides
                - One adjoint equation for the output variable X
        """
        result:list[Equation] = deepcopy(equations)
        uniqueInputs:list[Variable] = []

        # Find all unique right hand side 'inputs'
        for equation in equations:
            curRight:list[Monomial] = equation.right

            for monomial in curRight:
                variables:list[Variable] = monomial.variables

                for var in variables:
                    # Ignore if the variable is the function F
                    # Check if var is a duplicate in uniqueInputs
                    if var.name != constants.F and not any(Variable.isEqual(var, v) for v in uniqueInputs):
                        uniqueInputs.append(var)


        # Creates a new equation for each unique input
        for uniqueInput in uniqueInputs:
            newLeftVar:Variable = uniqueInput.derive(constants.ADJOINT, order=order)
            newEquation:Equation = Equation(newLeftVar, [], order=order)

            for equation in equations:
                newRightVar:Variable = equation.left.derive(constants.ADJOINT, order=order)

                for monomial in equation.right:
                    isIncluded:bool = False
                    newMonomial:Monomial = Monomial([])

                    for var in monomial.variables:
                        # Check if the variable in the current monomial is the unique input
                        if Variable.isEqual(var, uniqueInput):
                            isIncluded = True
                            pass
                        else:
                            newMonomial.variables.append(var)
                    
                    # If the unique input was in the right-hand side of this equation
                    if isIncluded:
                        newMonomial.variables.append(newRightVar)
                        newEquation.right.append(newMonomial)

            # Append the new equation for each unique input
            result.append(newEquation)

        
        # Form the output "X" equation
        newX:X = X(constants.ADJOINT, order=order)
        newEquation:Equation = Equation(left=newX, 
            right=[Monomial([F(order=order), Y(constants.ADJOINT, order=order)])], 
            order=order
        )
        for equation in equations:
            newRightVar:Variable = equation.left.derive(constants.ADJOINT, order=order)

            for monomial in equation.right:

                # The first element of a monomial is always the function f
                f:Variable = monomial.variables[0]
                newF:Variable = f.derive()

                # Append new monomials to the new adjoint output equation
                newMonomial:Monomial = Monomial([newF] + monomial.variables[1:] + [newRightVar])
                newEquation.right.append(newMonomial)

        # Append the new equation for the adjoint output
        result.append(newEquation)


        return result