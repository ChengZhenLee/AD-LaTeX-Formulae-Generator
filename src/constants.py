# Central constants shared across the AD formulae generator.
# Keeping LaTeX symbols and mode identifiers here avoids "magic string"
# duplication throughout src/notation and src/utils.

# Differentiation mode identifiers, as entered by the user in main.py
# (e.g. "ta" means "Tangent applied over Adjoint").
TANGENT = 't'
ADJOINT = 'a'

# Base variable names used throughout the notation classes (see
# src/notation/variable.py). F is the function being differentiated,
# X/Y are its input/output vectors.
F = 'F'
X = 'X'
Y = 'Y'

# LaTeX symbols used as the "running index" for adjoint (mu) and
# tangent (nu) derivatives, matching standard AD literature notation.
MU = '\\mu'
NU = '\\nu'

# The initial, undifferentiated equation y = F(x) that every derivation
# starts from, and the LaTeX line break used between equations in the
# generated align* environment.
START_EQUATION = "\\mathbf{y}_j &= F(\\mathbf{x}_i)"
LINEBREAK = "\\\\[1em]"

# Maps an equation's derivative order (mod UNIQUE_COLORS) to a LaTeX
# xcolor name, so that equations of the same order are colored
# consistently and colors cycle rather than run out for high orders.
ORDER_COLORS = {
    "0": "Black",
    "1": "Blue",
    "2": "Red",
    "3": "ForestGreen",
    "4": "Orange",
    "5": "RoyalPurple",
    "6": "Sepia",
}
UNIQUE_COLORS = 7

# Default base name (without extension) for the generated .tex file.
FILENAME = "Formulae"