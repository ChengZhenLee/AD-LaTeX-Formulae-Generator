# AD LaTeX Formulae Generator

A Python tool that symbolically derives and typesets the equations for
arbitrary-order **Algorithmic Differentiation (AD)** of a vector function
`y = F(x)`. Given any sequence of **Tangent** (forward-mode) and **Adjoint**
(reverse-mode) differentiation steps, it generates a ready-to-compile LaTeX
document containing the resulting derivative formulae, color-coded by order.

## How it works

Starting from the base equation `y_j = F(x_i)`, each mode you specify is
applied in sequence, left to right:

- **Tangent (`t`)** applies the product rule to propagate a directional
  derivative forward through the equation, introducing a new tangent input.
- **Adjoint (`a`)** applies the chain rule in reverse, generating one new
  equation per unique input variable that accumulates its sensitivity
  ("adjoint") from every equation it feeds into.

Modes can be mixed and nested to any order, e.g. `taa` computes the Tangent
derivative of the Adjoint-over-Adjoint (second-order reverse) derivative of
`F`. The mathematical implementation lives in
[src/DerivativeComputer.py](src/DerivativeComputer.py); the LaTeX notation
and rendering rules live in [src/notation/](src/notation/) and
[src/utils/](src/utils/).

## Requirements

- **Python 3.9 or later** (the code uses built-in generic type hints such as
  `list[Equation]`, which require Python 3.9+).
- No third-party packages — only the Python standard library.
- *Optional:* a LaTeX distribution (e.g. [TeX Live](https://www.tug.org/texlive/),
  [MiKTeX](https://miktex.org/), or [MacTeX](https://www.tug.org/mactex/)) if
  you want to compile the generated `.tex` file to a PDF. This is **not**
  required to run the generator itself.

## Usage

Clone or download the repository, then run the tool with one of the
platform-specific options below.

### Linux, macOS, WSL, or Git Bash on Windows

```bash
./run_tool.sh
```

(The script is already marked executable in the repository. If your
checkout ever loses that bit, restore it with `chmod +x run_tool.sh`.)

### Windows (Command Prompt or PowerShell)

```bat
run_tool.bat
```

### Any platform, directly with Python

```bash
python3 main.py      # Linux/macOS/WSL, or Windows if `python3` is on PATH
python main.py        # Windows (or any OS where `python` points to Python 3)
```

Once running, follow the terminal prompt:

1. Enter a string of `t` (Tangent) and `a` (Adjoint) characters describing
   the sequence of derivatives to compute, e.g. `taa`.
2. Press `e` at any time to exit.
3. The generated LaTeX source is written to `Formulae.tex` in the current
   directory (this file is intentionally left untracked by Git — see
   [.gitignore](.gitignore)).

### Example

Input `t` produces:

```latex
\begin{align*}
   \mathbf{y}_j &= F(\mathbf{x}_i) \\[1em]
   \color{Blue}{Y_{j,\nu_{1}}^{(1)}} & \color{Blue}{=} \ F_{j,i_{1}}^{[1]}\cdot X_{i_{1},\nu_{1}}^{(1)} \\[1em]
\end{align*}
```

To render the result as a PDF, compile it with any LaTeX engine, for example:

```bash
pdflatex Formulae.tex
```

## Project structure

```
main.py                        Interactive CLI entry point
run_tool.sh / run_tool.bat     Cross-platform launcher scripts
src/
├── constants.py                Shared LaTeX symbols and configuration
├── DerivativeComputer.py       Tangent/adjoint derivative algorithms
├── notation/
│   ├── index.py                 Index (subscript/superscript label) representation
│   ├── variable.py              Variable, and the X/Y/F helper subclasses
│   ├── monomial.py              Product-of-variables term representation
│   └── equation.py              Left/right-hand-side equation representation
└── utils/
    ├── TitleGenerator.py        Human-readable section titles
    └── LatexExporter.py         Assembles and writes the final .tex document
```

## Research context

This tool was built to support the visualizations in an
accompanying research paper:
> Naumann, U. (2026) Nested Algorithmic Differentiation Revisited
