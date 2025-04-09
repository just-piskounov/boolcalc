#!/usr/bin/env python
class BooleanAlgebra:
    def __init__(self):
        self.variables = set()
    
    class Term:
        def __init__(self, value, symbol):
            self.value = value  # 0 or 1
            self.symbol = symbol  # 'x', '~y', etc.
        
        def negate(self):
            new_value = 1 - self.value
            new_symbol = f"~{self.symbol}" if not self.symbol.startswith("~") else self.symbol[1:]
            return BooleanAlgebra.Term(new_value, new_symbol)
        
        def __str__(self):
            return self.symbol
        
        def __eq__(self, other):
            return self.symbol == other.symbol
        
        def __hash__(self):
            return hash(self.symbol)

    class Minterm:
        def __init__(self, terms):
            self.terms = terms
            self.symbol = "".join(str(t) for t in terms)
        
        def __str__(self):
            return "*".join(str(t) for t in self.terms)
        
        def get_binary(self, var_order):
            """Convert to binary representation (e.g., x~yz -> 101)"""
            binary = []
            for var in var_order:
                term_found = None
                for t in self.terms:
                    if t.symbol.replace("~", "") == var:
                        term_found = t
                        break
                if term_found:
                    binary.append("1" if not term_found.symbol.startswith("~") else "0")
                else:
                    binary.append("-")  # Don't care
            return "".join(binary)
        
        def can_combine(self, other, var_order):
            """Check if two minterms differ by one variable"""
            bin1 = self.get_binary(var_order)
            bin2 = other.get_binary(var_order)
            diff = sum(1 for b1, b2 in zip(bin1, bin2) if b1 != b2 and b1 != '-' and b2 != '-')
            return diff == 1

    @staticmethod
    def create_expression(input_str):
        """Create expression from string like '~x*y + x*~y + x*y'"""
        ba = BooleanAlgebra()
        minterms = []
        
        for product in input_str.split("+"):
            terms = []
            for factor in product.split("*"):
                factor = factor.strip()
                if factor.startswith("~"):
                    terms.append(ba.Term(0, factor))
                    ba.variables.add(factor[1:])
                else:
                    terms.append(ba.Term(1, factor))
                    ba.variables.add(factor)
            minterms.append(ba.Minterm(terms))
        
        return ba.Expression(minterms)

    class Expression:
        def __init__(self, minterms):
            self.minterms = minterms
        
        def simplify(self):
            if not self.minterms:
                return "0"
            
            var_order = sorted({t.symbol.replace("~", "") for m in self.minterms for t in m.terms})
            prime_implicants = self._find_prime_implicants(var_order)
            essential_primes = self._find_essential_primes(prime_implicants, var_order)
            return self._format_result(essential_primes, var_order)
        
        def _find_prime_implicants(self, var_order):
            """Quine-McCluskey step 1: Find all prime implicants"""
            groups = {}
            for m in self.minterms:
                ones = m.get_binary(var_order).count("1")
                groups.setdefault(ones, []).append(m)
            
            prime_implicants = []
            while True:
                new_groups = {}
                used = set()
                
                for ones in sorted(groups.keys()):
                    for m1 in groups.get(ones, []):
                        for m2 in groups.get(ones + 1, []):
                            if m1.can_combine(m2, var_order):
                                used.update([m1, m2])
                                combined = self._combine_minterms(m1, m2, var_order)
                                new_ones = combined.get_binary(var_order).count("1")
                                new_groups.setdefault(new_ones, []).append(combined)
                
                for ones in groups:
                    for m in groups[ones]:
                        if m not in used and m not in prime_implicants:
                            prime_implicants.append(m)
                
                if not new_groups:
                    break
                groups = new_groups
            
            return prime_implicants
        
        def _combine_minterms(self, m1, m2, var_order):
            """Combine two minterms that differ by one variable"""
            bin1 = m1.get_binary(var_order)
            bin2 = m2.get_binary(var_order)
            combined_bin = []
            terms = []
            
            for b1, b2, var in zip(bin1, bin2, var_order):
                if b1 == b2:
                    combined_bin.append(b1)
                    if b1 == "1":
                        terms.append(BooleanAlgebra.Term(1, var))
                    elif b1 == "0":
                        terms.append(BooleanAlgebra.Term(0, f"~{var}"))
                else:
                    combined_bin.append("-")
            
            return BooleanAlgebra.Minterm(terms)
        
        def _find_essential_primes(self, prime_implicants, var_order):
            """Quine-McCluskey step 2: Find essential prime implicants"""
            chart = {m: [] for m in self.minterms}
            for pi in prime_implicants:
                for m in self.minterms:
                    if self._covers(pi, m, var_order):
                        chart[m].append(pi)
            
            essential = []
            for m in self.minterms:
                if len(chart[m]) == 1:
                    pi = chart[m][0]
                    if pi not in essential:
                        essential.append(pi)
            
            return essential
        
        def _covers(self, pi, m, var_order):
            """Check if prime implicant covers a minterm"""
            pi_bin = pi.get_binary(var_order)
            m_bin = m.get_binary(var_order)
            
            for p, m in zip(pi_bin, m_bin):
                if p != "-" and p != m:
                    return False
            return True
        
        def _format_result(self, primes, var_order):
            """Convert prime implicants to readable expression"""
            if not primes:
                return "0"
            
            terms = []
            for pi in primes:
                product = []
                pi_bin = pi.get_binary(var_order)
                for bit, var in zip(pi_bin, var_order):
                    if bit == "1":
                        product.append(var)
                    elif bit == "0":
                        product.append(f"~{var}")
                if product:
                    terms.append("*".join(product))
            
            return " + ".join(terms) if terms else "1"
        
        def __str__(self):
            return " + ".join(str(m) for m in self.minterms)

# Extensive Examples
if __name__ == "__main__":
    examples = [
        # Basic examples
        ("x*y + ~x*y + x*~y", "x + y"),
        ("x*y*z + x*y*~z", "x*y"),
        ("~x*~y + ~x*y + x*~y", "~x + ~y"),
        
        # 3-variable examples
        ("x*y*z + x*y*~z + x*~y*z + ~x*y*z", "x*z + y*z + x*y"),
        ("~x*~y*~z + ~x*~y*z + ~x*y*z + x*~y*z", "~x*~y + ~x*z + ~y*z"),
        
        # With don't-care conditions (not fully implemented but structure is ready)
        ("x*y + x*~y + ~x*~y", "x + ~y"),
        
        # Edge cases
        ("x", "x"),  # Single variable
        ("x + ~x", "1"),  # Tautology
        ("x*~x", "0")  # Contradiction
    ]
    
    print("BOOLEAN EXPRESSION SIMPLIFIER")
    print("=" * 50)
    
    for original, expected in examples:
        print(f"\nOriginal: {original}")
        expr = BooleanAlgebra.create_expression(original)
        simplified = expr.simplify()
        print(f"Simplified: {simplified}")
        print(f"Expected: {expected}")
        print("-" * 50)
    
    # Interactive demo
    while True:
        print("\nEnter a boolean expression to simplify (or 'q' to quit):")
        print("Example format: x*y + ~x*z + y*~z")
        user_input = input("> ").strip()
        
        if user_input.lower() == 'q':
            break
            
        try:
            expr = BooleanAlgebra.create_expression(user_input)
            print(f"Original: {expr}")
            simplified = expr.simplify()
            print(f"Simplified: {simplified}")
        except Exception as e:
            print(f"Error: {e}. Please check your input format.")
