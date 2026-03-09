from src.notation.equation import Equation
from src.constants import START_EQUATION, LINEBREAK, FILENAME


class LatexExporter:
    @staticmethod
    def createLatex(equations: list[Equation], filename: str = FILENAME) -> None:
        """Generate a LaTeX document containing mathematical equations.
        This function creates a .tex file with a formatted LaTeX document that displays
        a collection of equations, starting with an initial equation and followed by
        calculated derivative equations.

        Args:
            equations (list[Equation]): A list of Equation objects representing the
                calculated derivatives or related equations to be included in the document.
            filename (str, optional): The name of the output .tex file (without extension).
                The file will be created as "{filename}.tex" in the current working directory.
        """
        
        content = [
            "\\documentclass{article}",
            "\\usepackage[utf8]{inputenc}",
            "\\usepackage{amsmath}",
            "\\usepackage[margin=1in]{geometry}",
            "\\usepackage[dvipsnames]{xcolor}",
            "\\allowdisplaybreaks",
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