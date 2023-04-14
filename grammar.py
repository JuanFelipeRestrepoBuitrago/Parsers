import re


# Class to handle the grammar
class Grammar:
    # Constructor defining the elements of the grammar
    def __init__(self):
        self.productions = {}
        self.start = None
        self.non_terminals = set()
        self.terminals = set()

    # Method to add a production to the grammar
    def add_production(self, symbol: str, derivation: str):
        # If the symbol is not in the productions, it is new, so we add it
        if symbol not in self.productions:
            self.productions[symbol] = []
        # We add the derivation to the symbol
        self.productions[symbol].append(derivation)

    # Method to delete a production from the grammar
    def delete_production(self, symbol: str, derivation: str):
        # If the symbol is not in the productions or the derivation is not in the productions of the symbol,
        # it is not in the grammar, so we return None
        if symbol not in self.productions or derivation not in self.productions[symbol]:
            return None
        # We remove the derivation from the symbol
        self.productions[symbol].remove(derivation)

    # Method to delete a production, receiving the production as a string
    def delete_production_str(self, production: str):
        # We create a pattern to match the productions of the form: A -> aB|ε and
        # to make the separation of the symbol and the derivations easier
        pattern = re.compile(r'\s*(?P<Symbol>[A-Z]\'*)\s?->\s?(?P<Derivations>.+)')

        # We match the production with the pattern
        production_match = pattern.match(production)
        # If the production does not match the pattern, it is invalid
        if not production_match:
            raise SyntaxError("Invalid production: {}, It should be of the form: A -> aB|ε".format(production))
        # Retrieve the symbol and the derivations from the match
        symbol = production_match.group("Symbol")
        derivations = production_match.group("Derivations")

        # Split the derivations by the '|' symbol, making it an array
        derivations = derivations.split('|')
        # For each derivation, we delete it from the grammar
        for derivation in derivations:
            self.delete_production(symbol, derivation)

    # Method to receive a production from the console or from a parameter
    def receive_production(self, production: str = None):
        # If the production is not given, we ask for it through the console
        if production is None:
            production = input("Enter a production: ")

        # We create a pattern to match the productions of the form: A -> aB|ε and
        # to make the separation of the symbol and the derivations easier
        pattern = re.compile(r'\s*(?P<Symbol>[A-Z]\'*)\s?->\s?(?P<Derivations>.+)')

        # We match the production with the pattern
        production_match = pattern.match(production)
        # If the production does not match the pattern, it is invalid
        if not production_match:
            raise SyntaxError("Invalid production: {}, It should be of the form: A -> aB|ε".format(production))
        # Retrieve the symbol and the derivations from the match
        symbol = production_match.group("Symbol")
        derivations = production_match.group("Derivations")

        # Add the symbol to the non-terminals
        self.add_non_terminal(symbol)
        # Split the derivations by the '|' symbol, making it an array
        derivations = derivations.split('|')
        # For each derivation, we add it to the grammar
        for derivation in derivations:
            self.add_production(symbol, derivation)

            # We create a pattern to match the non-terminals in the derivation
            pattern = re.compile(r'([A-Z]\'*)')
            # We match the derivation with the pattern, adding the non-terminals to the grammar
            # and removing them from the derivation
            for _ in pattern.finditer(derivation):
                element = pattern.search(derivation)
                self.add_non_terminal(element.group(1))
                derivation = derivation[:element.start()] + derivation[element.end():]

            # For each element in the derivation, we check if it is a non-terminal or a terminal,
            # and we add it to the corresponding set
            for element in range(len(derivation)):
                self.add_terminal(derivation[element])

    # Method to add a non-terminal to the grammar, it does not matter if it is already in the grammar
    # the set does not allow duplicates
    def add_non_terminal(self, non_terminal: str):
        if re.match(r'[A-Z]\'*', non_terminal):
            self.non_terminals.add(non_terminal)
        else:
            raise SyntaxError("Non-terminal must be an uppercase letter followed by 0 or more apostrophes")

    # Method to add a terminal to the grammar, it does not matter if it is already in the grammar
    # the set does not allow duplicates
    def add_terminal(self, terminal: str):
        if terminal != 'ε':
            self.terminals.add(terminal)

    # Method to set the start symbol of the grammar
    def set_start(self, start: str):
        # We check if the start symbol is a non-terminal, if not, we add it
        try:
            if start not in self.non_terminals:
                raise ValueError("Start symbol must be a non-terminal")
        except ValueError:
            self.add_non_terminal(start)
        # We set the start symbol
        self.start = start

    # Method to print the productions of the grammar in case we want to print the grammar
    def __str__(self):
        grammar_str = ""
        # For each non-terminal in the productions, we add the non-terminal and the derivations to the string
        for symbol in self.productions:
            # We add the non-terminal and the arrow
            grammar_str += symbol + " -> "
            # For each derivation, we add it to the string separated by a '|'
            for derivation in self.productions[symbol]:
                grammar_str += derivation + "|"
            # We remove the last '|' and add a new line, so the next non-terminal is in the next line
            grammar_str = grammar_str[:-1] + "\n"
        grammar_str += "Start symbol: " + self.start
        return grammar_str
