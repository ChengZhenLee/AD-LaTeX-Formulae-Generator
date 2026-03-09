from src.notation.equation import Equation
from src.constants import START_EQUATION, LINEBREAK


class LatexExporter:
    @staticmethod
    def createLatex(equations:list[Equation], filename:str="Derivatives"):
        content = [
            "\\documentclass{article}",
            "\\usepackage[utf8]{inputenc}",
            "\\usepackage{amsmath}",
            "\\usepackage[margin=1in]{geometry}",
            "\\begin{document}",
            "\\section*{Generated Derivatives}",
            "\\begin{align*}"
        ]

        # Include the starting equation y=f(x)
        content.append(f"   {START_EQUATION} {LINEBREAK}")

        # Include the calculated equations
        for equation in equations:
            content.append(f"   {equation} {LINEBREAK}")

        content += ["\\end{align*}", "\\end{document}"]

        with open(f"{filename}.tex", 'w') as outFile:
            outFile.write("\n".join(content))
        outFile.close()