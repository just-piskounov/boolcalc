# BoolCalc

A Boolean algebra calculator with both CLI and GUI interfaces.

## Description

BoolCalc is a Python tool that allows you to work with Boolean expressions. It can simplify Boolean expressions and generate truth tables through both a command-line interface and a terminal-based GUI powered by Textual.

## Features

- Parse and evaluate Boolean expressions
- Generate truth tables for expressions
- Simplify Boolean expressions using the Quine-McCluskey algorithm
- Terminal-based GUI interface
- Support for basic Boolean operators:
  - AND (`*`)
  - OR (`+`)
  - NOT (`~`)

## Installation

```bash
# Requires Python 3.10 or higher
pip install boolcalc
```

Or install from source:

```bash
git clone https://github.com/just-piskounov/boolcalc.git
cd boolcalc
pip install .
```

## Usage

### GUI Version

Launch the interactive terminal UI:

```bash
boolcalc
```

### CLI Version

You can also use the package programmatically:

```python
from boolcalc.core import BooleanExpression

# Create a Boolean expression
expr = BooleanExpression("x*y + ~x*z")

# Simplify the expression
simplified = expr.simplify()
print(f"Simplified: {simplified}")

# Generate a truth table
variables = sorted(expr.get_variables())
print(" | ".join(variables + ["Result"]))
print("-" * (len(variables) * 4 + 8))

from itertools import product
for values in product([False, True], repeat=len(variables)):
    inputs = dict(zip(variables, values))
    result = expr.evaluate(inputs)
    values_str = " | ".join(str(int(v)) for v in values)
    print(f"{values_str} | {int(result)}")
```

## Dependencies

- textual >= 0.34.0
- rich >= 13.0

## License

Open source
