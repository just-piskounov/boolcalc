# BoolCalc

A command-line utility for evaluating boolean expressions and generating truth tables.

## Overview

BoolCalc is a lightweight tool designed to parse and evaluate boolean expressions with support for variables, logical operators, and truth table generation. Perfect for students learning boolean algebra, computer science enthusiasts, or anyone who needs to quickly validate boolean logic.

## Features

- Parse and evaluate boolean expressions with variables
- Generate complete truth tables for expressions
- Support for standard boolean operators:
  - AND (∧, &, *)
  - OR (∨, |, +)
  - NOT (¬, ~, !)
  - XOR (⊕, ^)
  - Implication (→, ->)
  - Biconditional/Equivalence (↔, <->)
- Parentheses for expression grouping
- Variable auto-detection

## Installation

Ensure you have Python 3.6+ installed, then:

```bash
# Clone the repository
git clone https://github.com/just-piskounov/boolcalc.git
cd boolcalc

# Install dependencies (if any)
# pip install -r requirements.txt
```

## Usage

### Basic Boolean Expression Evaluation

```bash
python boolcalc.py "A & B | ~C"
```

### Generate Truth Table

```bash
python boolcalc.py "A -> (B & C)" --table
```

### Available Operators

| Operation    | Symbols      | Precedence |
|--------------|--------------|------------|
| NOT          | ¬, ~, !      | Highest    |
| AND          | ∧, &, *      | High       |
| XOR          | ⊕, ^         | Medium     |
| OR           | ∨, \|, +     | Medium     |
| Implication  | →, ->        | Low        |
| Biconditional| ↔, <->       | Lowest     |

## Examples

### Simple Expression
```bash
python boolcalc.py "A & B"
```

### Complex Expression with Multiple Variables
```bash
python boolcalc.py "(A | B) & ~(C -> D)"
```

### Truth Table for an Expression
```bash
python boolcalc.py "A ^ B" --table
```

Output:
```
| A | B | A ^ B |
|---|---|-------|
| 0 | 0 |   0   |
| 0 | 1 |   1   |
| 1 | 0 |   1   |
| 1 | 1 |   0   |
```

## Contributing

Contributions are welcome! Feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Created by [just-piskounov](https://github.com/just-piskounov)
