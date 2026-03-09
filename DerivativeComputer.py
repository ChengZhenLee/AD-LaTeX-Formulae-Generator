from copy import deepcopy
from equation import Equation
from term import Term
from variable import Variable, X, Y, F
import constants


class DerivativeComputer(): 
    @staticmethod
    def computeDerivative(modes:str, equations:list[Equation]=[])->list[Equation]:
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
        result:list[Equation] = deepcopy(equations)

        # Perform tangent mode on the existing equations
        for equation in equations:
            newLeftVar:Variable = equation.left.derive(constants.TANGENT, order=order)
            newEquation:Equation = Equation(newLeftVar, [], order=order)
            
            for term in equation.right:
                for i, var in enumerate(term.variables):
                    newTerm:Term = Term([])
                    newVar:Variable = var.derive(constants.TANGENT, order=order)

                    tempVar:list[Variable] = term.variables.copy()
                    tempVar.pop(i)

                    if var.name == constants.F:
                        # The function F should always be at the front
                        newTerm.variables = [newVar]
                        newTerm.variables += tempVar
                        newTerm.variables.append(X(constants.TANGENT, order=order))
                    else:
                        newTerm.variables = tempVar
                        newTerm.variables.append(newVar)
                    
                    newEquation.right.append(newTerm)

            result.append(newEquation)

        
        # Append the additional tangent "Y" equation
        newEquation:Equation = Equation(
            Y(constants.TANGENT, order=order),
            right=[Term([F(order=order), X(constants.TANGENT, order=order)])],
            order=order
        )
        result.append(newEquation)

        return result

    
    @staticmethod
    def _adjointMode(equations:list[Equation], order:str)->list[Equation]:
        result:list[Equation] = deepcopy(equations)
        uniqueInputs:list[Variable] = []

        # Find all unique right hand side 'inputs'
        for equation in equations:
            curRight:list[Term] = equation.right

            for term in curRight:
                variables:list[Variable] = term.variables

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

                for term in equation.right:
                    isIncluded:bool = False
                    newTerm:Term = Term([])

                    for var in term.variables:
                        # Check if the variable in the current term is the unique input
                        if Variable.isEqual(var, uniqueInput):
                            isIncluded = True
                            pass
                        else:
                            newTerm.variables.append(var)
                    
                    # If the unique input was in the right-hand side of this equation
                    if isIncluded:
                        newTerm.variables.append(newRightVar)
                        newEquation.right.append(newTerm)

            # Append the new equation for each unique input
            result.append(newEquation)

        
        # Form the output "X" equation
        newX:X = X(constants.ADJOINT, order=order)
        newEquation:Equation = Equation(left=newX, 
            right=[Term([F(order=order), Y(constants.ADJOINT, order=order)])], 
            order=order
        )
        for equation in equations:
            newRightVar:Variable = equation.left.derive(constants.ADJOINT, order=order)

            for term in equation.right:

                # The first element of a term is always the function f
                f:Variable = term.variables[0]
                newF:Variable = f.derive()

                # Append new terms to the new adjoint output equation
                newTerm:Term = Term([newF] + term.variables[1:] + [newRightVar])
                newEquation.right.append(newTerm)

        # Append the new equation for the adjoint output
        result.append(newEquation)


        return result