from constants import STARTEQUATION, LINEBREAK
from DerivativeComputer import DerivativeComputer
from equation import Equation


def main():
    isValid:bool = False
    inputModes:str = ""
    while (not isValid):
        userInput:str = input("Enter derivative modes e.g. 'taa' for Tangent over Adjoint over Adjoint\n" \
        "Press 'e' to exit: \n")
        inputModes = userInput.lower().strip()

        if inputModes and all(char in ['t', 'a'] for char in inputModes):
            print('-'*30)
            print(STARTEQUATION)
            print(LINEBREAK)

            equations:list[Equation] = DerivativeComputer.computeDerivative(inputModes, [])
            for equation in equations:
                print(equation)
                print(LINEBREAK)
            print('-'*30)
            
        
        elif inputModes == 'e':
            break


if __name__ == "__main__":
    main()