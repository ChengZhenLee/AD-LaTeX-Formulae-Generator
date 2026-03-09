from variable import Variable


class Term:
    def __init__(self, variables:list[Variable]):
        self.variables = variables

    
    def __str__(self)->str:
        variableStr:str = "\\cdot ".join([str(v) for v in self.variables])

        return variableStr if variableStr else ""