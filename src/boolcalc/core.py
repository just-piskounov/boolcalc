from typing import List, Set, Dict, Tuple
from itertools import product

class Term:
    def __init__(self, symbol: str, is_negated: bool = False):
        self.symbol = symbol.strip()
        self.is_negated = is_negated

    def evaluate(self, inputs: Dict[str, bool]) -> bool:
        value = inputs.get(self.symbol, False)
        return not value if self.is_negated else value

    def __repr__(self):
        return f"~{self.symbol}" if self.is_negated else self.symbol

class BooleanExpression:
    def __init__(self, expression: str):
        self.raw_expression = expression
        self.terms = self._parse_expression(expression)
    
    def _parse_expression(self, expr: str) -> List[List[Term]]:
        or_groups = []
        for group in expr.lower().split('+'):
            and_terms = []
            for factor in group.split('*'):
                factor = factor.strip()
                if not factor: continue
                is_negated = factor.startswith('~')
                symbol = factor[1:] if is_negated else factor
                and_terms.append(Term(symbol, is_negated))
            if and_terms:
                or_groups.append(and_terms)
        return or_groups

    def get_variables(self) -> Set[str]:
        return {term.symbol for group in self.terms for term in group}

    def evaluate(self, inputs: Dict[str, bool]) -> bool:
        return any(
            all(term.evaluate(inputs) for term in group)
            for group in self.terms
        )

    def simplify(self) -> str:
        variables = sorted(self.get_variables())
        num_vars = len(variables)
        minterms = set()
        
        for values in product([False, True], repeat=num_vars):
            inputs = dict(zip(variables, values))
            if self.evaluate(inputs):
                minterm = sum(2**i for i, val in enumerate(reversed(values)) if val)
                minterms.add(minterm)
        
        if not minterms: return "0"
        if len(minterms) == 2**num_vars: return "1"
        
        primes = self._find_prime_implicants(minterms, num_vars)
        essentials = self._find_essential_primes(primes, minterms)
        return self._format_expression(essentials, variables)

    def _find_prime_implicants(self, minterms: Set[int], num_vars: int) -> List[Tuple[Set[int], str]]:
        groups = {}
        for m in minterms:
            binary = bin(m)[2:].zfill(num_vars)
            ones = binary.count('1')
            groups.setdefault(ones, []).append(({m}, binary))
        
        primes = []
        while True:
            new_groups = {}
            used = set()
            for ones in sorted(groups):
                for (m1_set, bin1) in groups[ones]:
                    for (m2_set, bin2) in groups.get(ones+1, []):
                        if sum(b1 != b2 for b1, b2 in zip(bin1, bin2)) == 1:
                            used.update([(frozenset(m1_set), bin1), (frozenset(m2_set), bin2)])
                            new_bin = ''.join('-' if b1 != b2 else b1 for b1, b2 in zip(bin1, bin2))
                            new_groups.setdefault(ones, []).append((m1_set | m2_set, new_bin))
            
            for group in groups.values():
                for (m_set, bin_str) in group:
                    if (frozenset(m_set), bin_str) not in used:
                        primes.append((m_set, bin_str))
            
            if not new_groups: break
            groups = new_groups
        
        return primes

    def _find_essential_primes(self, primes: List[Tuple[Set[int], str]], minterms: Set[int]) -> List[Tuple[Set[int], str]]:
        coverage = {m: [] for m in minterms}
        for (m_set, bin_str) in primes:
            for m in m_set & minterms:
                coverage[m].append((m_set, bin_str))
        
        essentials = []
        covered = set()
        for m, covers in coverage.items():
            if len(covers) == 1:
                prime = covers[0]
                if prime not in essentials:
                    essentials.append(prime)
                    covered.update(prime[0])
        
        remaining = minterms - covered
        while remaining:
            best_prime = max(
                (p for p in primes if p[0] & remaining),
                key=lambda p: len(p[0] & remaining),
                default=None
            )
            if best_prime:
                essentials.append(best_prime)
                covered.update(best_prime[0])
                remaining = minterms - covered
        
        return essentials

    def _format_expression(self, primes: List[Tuple[Set[int], str]], variables: List[str]) -> str:
        terms = []
        for _, binary in primes:
            term = []
            for var, bit in zip(variables, binary):
                if bit == '1': term.append(var)
                elif bit == '0': term.append(f"~{var}")
            if term: terms.append('*'.join(term))
        return ' + '.join(terms) if terms else '0'
