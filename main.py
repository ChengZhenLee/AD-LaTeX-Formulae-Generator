"""Interactive command-line entry point for the AD formulae generator.

Prompts the user for a sequence of differentiation modes (Tangent/Adjoint),
computes the resulting derivative equations, and writes them to a LaTeX
file. Run via `python main.py` (or `run_tool.sh` / `run_tool.bat`).
"""

from src.DerivativeComputer import DerivativeComputer
from src.utils.LatexExporter import LatexExporter
from src.utils.TitleGenerator import TitleGenerator
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

        # Only accept strings made up of 't' (Tangent) and 'a' (Adjoint);
        # each character is applied left-to-right as one differentiation step.
        if inputModes and all(char in "ta" for char in inputModes):
            equations:list[Equation] = DerivativeComputer.computeDerivative(inputModes, [])
            title:str = TitleGenerator.generateTitle(inputModes)
            LatexExporter.createLatex(title, equations, FILENAME)
            print(f"LaTeX file generated as {FILENAME}.tex")
        else:
            print("Error: Use only 't' (Tangent) or 'a' (Adjoint), or 'e' to exit")

        print()


if __name__ == "__main__":
    runTool()