from src.DerivativeComputer import DerivativeComputer
from src.utils.LatexExporter import LatexExporter
from utils.TitleGenerator import TitleGenerator
from src.notation.equation import Equation
from src.constants import FILENAME


def runTool():
    print("======================================")
    print("   AD DERIVATIVE FORMULAE GENERATOR   ")
    print("======================================")

    while (True):
        userInput:str = input("Enter derivative modes (e.g. 'taa' for Tangent over Adjoint over Adjoint) " \
        "or press 'e' to exit: \n")
        inputModes = userInput.lower().strip()

        if inputModes == "e":
            break
        
        if inputModes and all(char in "ta" for char in inputModes):
            equations:list[Equation] = DerivativeComputer.computeDerivative(inputModes, [])
            title:str = TitleGenerator.generateTitle(inputModes)
            LatexExporter.createLatex(title, equations, FILENAME)
            print(f"LaTeX file generated as {FILENAME}.tex")
        else:
            print("Error: Use only 't' (Tangent) or 'a' (Adjoint).")

        print()


if __name__ == "__main__":
    runTool()