from __future__ import annotations
from src.notation.index import Index
import src.constants as constants


class Variable:
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
    def __init__(self, order:str='1', indices:list[Index]=[], derived:str='1'):
        self.derived = derived
        if len(indices) == 0:
            indices = [Index('j', '0'), Index('i', order)]

        super().__init__(constants.F, indices, sub=[], sup=[], order=order) 

    
    def derive(self, mode:str="", order:str="1")->F:
        newOrder = str(int(self.order) + 1)
        newDerived = str(int(self.derived) + 1)

        newIndices = self.indices + [Index('i', newOrder)]

        return F(order=newOrder, indices=newIndices, derived=newDerived)
    

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
