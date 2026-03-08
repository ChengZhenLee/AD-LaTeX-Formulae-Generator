from equation import Equation
from term import Term
from variable import Variable
from index import Index
import constants


class DerivativeComputer(): 
    @staticmethod
    def computeDerivative(modes:list[str], equations:list[Equation]=[])->list[Equation]:
        order = len(modes)

        # base case
        if order == 0:
            return equations
        
        # recursive
        mode = modes[0]
        rest = modes[1:]
        result = DerivativeComputer.computeDerivative(rest, equations)

        if mode == constants.TANGENT:
            result = DerivativeComputer._tangentMode(result, order)
        elif mode == constants.ADJOINT:
            result = DerivativeComputer._adjointMode(result, order)

        print(result)
        return result
        
    
    @staticmethod
    def _tangentMode(equations:list[Equation], order:int)->list[Equation]:
        return []

    
    @staticmethod
    def _adjointMode(equations:list[Equation], order:int)->list[Equation]:
        result:list[Equation] = equations[:]
        uniqueInputs:list[Variable]=[]

        # Find all unique right hand side 'inputs'
        for equation in equations:
            curRight:list[Term] = equation.right

            for term in curRight:
                variables:list[Variable] = term.variables

                for var in variables:
                    is_duplicate = any(
                        DerivativeComputer.checkIsDuplicateVariable(var, v)
                        for v in uniqueInputs
                    )

                    if not is_duplicate:
                        uniqueInputs.append(var)
            


        newLeft = Variable(
            name=constants.X,
            indices=[Index(constants.MU, order), Index('i', order)],
            sub=[str(order)])
        

        return []
    

    @staticmethod
    def checkIsDuplicateVariable(v1:Variable, v2:Variable)->bool:
        return (
            v1.name == v2.name and
            v1.sub == v2.sub and
            v1.sup == v2.sup
        )