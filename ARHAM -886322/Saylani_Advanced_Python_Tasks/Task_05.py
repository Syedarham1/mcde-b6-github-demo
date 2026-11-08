import re
def evaluate_expression(expr):
    # Tokenizer
    token_pattern = re .compile(r'\s*([0-9]+(?:\.[0-9]+)?|\+|\-|\*|\/|\(|\))\s*')
    tokens = [match.group(1) for match in token_pattern.finditer(expr)]
    
    if not tokens or "".join(tokens) != expr.replace(" ", ""):
        raise ValueError("Malformed expression")

    def parse_tokens(toks):
        # Shunting-yard or recursive descent parser
        pass # implemented with robust recursive descent below

    # Implementing a clean recursive descent parser for expr
    class Parser:
        def __init__(self, s):
            self.tokens = re.findall(r'[0-9]+(?:\.[0-9]+)?|\+|\-|\*|\/|\(|\)', s)
            self.pos = 0

        def peek(self):
            return self.tokens[self.pos] if self.pos < len(self.tokens) else None

        def consume(self):
            tok = self.peek()
            self.pos += 1
            return tok

        def parse(self):
            val = self.expr()
            if self.pos < len(self.tokens):
                raise ValueError("Unexpected tokens")
            return val

        def factor(self):
            tok = self.consume()
            if tok is None:
                raise ValueError("Unexpected end of expression")
            if tok == '(':
                val = self.expr()
                if self.consume() != ')':
                    raise ValueError("Mismatched parentheses")
                return val
            elif tok == '-':
                return -self.factor()
            elif tok == '+':
                return self.factor()
            else:
                try:
                    return float(tok)
                except ValueError:
                    raise ValueError(f"Invalid token: {tok}")

        def term(self):
            val = self.factor()
            while self.peek() in ('*', '/'):
                op = self.consume()
                next_val = self.factor()
                if op == '*':
                    val *= next_val
                elif op == '/':
                    if next_val == 0:
                        raise ZeroDivisionError("Division by zero")
                    val /= next_val
            return val

        def expr(self):
            val = self.term()
            while self.peek() in ('+', '-'):
                op = self.consume()
                next_val = self.term()
                if op == '+':
                    val += next_val
                elif op == '-':
                    val -= next_val
            return val

    parser = Parser(expr.replace(" ", ""))
    return parser.parse()

if __name__ == "__main__":
    print(evaluate_expression("-(3 + 2) * 4 + 18 / 3"))  