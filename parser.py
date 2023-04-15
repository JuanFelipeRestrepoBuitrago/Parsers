from grammar import Grammar
import re


# Parent class for all parsers
class Parser:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar

# Function to calculate the first of a symbol or string
    def first(self, string: str, visited: set = None):
        # Set of non-terminals that have been visited in the recursion
        if visited is None:
            visited = set()
        first = set()
        # Check if the string is a non-terminal
        if string in self.grammar.non_terminals:
            # Check if the non-terminal has been visited to add it to the visited set
            if string not in visited:
                visited.add(string)
            # We must check the first of each derivation of the non-terminal
            for derivation in self.grammar.productions[string]:
                first = self.first_string(derivation, first, visited, string)
        # Check if the string is a terminal to add it to the first set and return it directly
        elif string in self.grammar.terminals:
            first.add(string)
            return first
        # Check if the string is epsilon to add it to the first set and return it directly
        elif string == "ε":
            first.add("ε")
            return first
        # Check if the string is a string of more than one character
        elif len(string) > 1:
            first = self.first_string(string, first, visited)
        # If none of the above conditions is true, then the string is not in the grammar
        else:
            raise SyntaxError("Symbol {} is not in the grammar".format(string))

        return first

    # Function to calculate the first of a string
    def first_string(self, string: str, first: set, visited: set, symbol: str = None):
        if symbol is None:
            symbol = ''
        pattern = re.compile(r"[A-Z]\'+")
        element = 0
        while element < len(string):
            # Check if the current character is a non-terminal with a single quote (A'),
            # in this case, we need to check the first of the non-terminal with the single quote (A')
            # and add 1 to the element to check the next character's first of the string
            if element <= len(string) - 2 and pattern.match(string[element] + string[element + 1]):
                if string[element] + string[element + 1] == symbol or string[element] + string[element + 1] in visited:
                    return first
                first_of_element = self.first(string[element] + string[element + 1], visited)
                element += 1
            else:
                if string[element] == symbol or string[element] in visited:
                    return first
                first_of_element = self.first(string[element], visited)

            if "ε" in first_of_element:
                # Adds the first of the current character to the first of the symbol except epsilon
                first_of_element.remove("ε")
                first = first.union(first_of_element)
                # If the current character is the last one, then add epsilon to the first of the symbol
                # This is because the first of all symbols in string contains epsilon
                if element == len(string) - 1:
                    first.add("ε")
            else:
                # If the current character does not contain epsilon, then add the first of the current character to
                # the first of the symbol
                first = first.union(first_of_element)
                break
            element += 1

        return first

    @staticmethod
    # Method insert every element of the first set in the follow set except epsilon
    def join_first_follow(first: set, follow: set):
        if "ε" in first:
            first.remove("ε")
            # Returns the union of the first and follow sets,
            # so the follow set will contain its elements and the first set without epsilon
            follow = follow.union(first)
            # Add epsilon to the first set, because the first set contains epsilon
            first.add("ε")
            return follow
        else:
            return first.union(follow)

    # Function to calculate the first two rules of the follow function
    def follow_one_two(self, symbol):
        follow = set()
        # If the symbol is the start symbol, then add $ to the follow set
        # rule 1, $ ∈ follow(S)
        if symbol == self.grammar.start:
            follow.add("$")
        # We must check every derivation of every non-terminal
        for non_terminal, derivations in self.grammar.productions.items():
            for derivation in derivations:
                # Check if the symbol is in the derivation, and it does not have a single quote (A')
                # if it has a single quote, then it is not the same symbol, for example, A' != A and A'' != A'
                pattern = symbol + r"(?!\')"
                for _ in re.finditer(pattern, derivation):
                    # Get the index of the symbol in the derivation, the last index of the symbol, for example, if the
                    # symbol is A' and the derivation is A'BC, then the index will be 1
                    index = derivation.index(symbol) + len(symbol) - 1
                    # If the symbol is not the last character of the derivation
                    if index != len(derivation) - 1:
                        # First of β
                        first = self.first(derivation[index + 1:])
                        # Rule 2, A -> αBβ; all in first(β) are in follow(B) except epsilon
                        follow = self.join_first_follow(first, follow)
                    # We erase the symbol from the derivation, so we can find the next occurrence of the symbol
                    derivation = derivation[:derivation.index(symbol)] + derivation[index + 1:]

        return follow

    # Function to calculate the third rule of the follow function, the restrictions of it
    def follow_third(self):
        # Dictionary to store the subsets of the non-terminals
        subsets = {self.grammar.start: set()}
        for non_terminal in self.grammar.non_terminals:
            if non_terminal != self.grammar.start:
                subsets[non_terminal] = set()
        # We must check every derivation of every non-terminal
        for non_terminal, derivations in self.grammar.productions.items():
            for derivation in derivations:
                # We must check if the non-terminal is on the right side of the derivation
                pattern = re.compile(r".*([A-Z]\'*)$")
                match = pattern.match(derivation)
                while match:
                    # If the right side non-terminal is not the same as the principal non-terminal
                    if match.group(1) != non_terminal:
                        # Add the right side non-terminal to the principal non-terminal subset, meaning that the
                        # follow of the principal non-terminal is the follow of the right side non-terminal
                        subsets[non_terminal].add(match.group(1))
                    # If the right side non-terminal first set contains epsilon
                    # then we must check the next right side non-terminal,
                    # but before we must remove the right side non-terminal from the derivation
                    if self.first(match.group(1)).__contains__("ε"):
                        derivation = derivation[:match.end() - len(match.group(1))]
                    else:
                        # If the right side non-terminal first set does not contain epsilon, then we must
                        # stop the loop
                        break
                    match = pattern.match(derivation)
        return subsets

    # Check if there is a loop in the third rule of the follow function
    def check_loop(self, main_non_terminal, non_terminal, subsets, visited=None):
        # Initialize the visited set if it is None
        if visited is None:
            visited = set()
        # Add the main non-terminal to the visited set
        visited.add(main_non_terminal)
        # Loop through the subset of the main non-terminal
        for current_non_terminal in subsets[main_non_terminal]:
            # If the non-terminal is in the subset of the main non-terminal, then there is a loop
            if current_non_terminal == non_terminal:
                return True
            # If the non-terminal is not in the visited set, then we must check if there is a loop in the subset with
            # the current non-terminal
            elif current_non_terminal not in visited:
                if self.check_loop(current_non_terminal, non_terminal, subsets, visited):
                    return True
        return False

    # Function to calculate the follow of a symbol
    def follow(self, symbol):
        # Retrieve the follow of the symbol using the first two rules
        follow = self.follow_one_two(symbol)
        # Retrieve the subsets of the non-terminals to check the third rule
        subsets = self.follow_third()
        # We must check every subset of the non-terminals
        for principal, sub in subsets.items():
            # If the symbol is in the subset, then we must add the follow of the principal non-terminal
            # to the follow of the symbol
            if symbol in sub:
                # If the principal non-terminal is in the subset of the symbol, then we must add the follow of the
                # principal non-terminal to the follow of the symbol, without recursion to avoid infinite loops
                if self.check_loop(symbol, principal, subsets):
                    follow_of_principal = self.follow_one_two(principal)
                    # If the follow of the principal non-terminal is not empty, then we must add it to the follow
                    if len(follow_of_principal) > 0:
                        follow = follow.union(follow_of_principal)
                    else:
                        # If the follow of the principal non-terminal is empty, then we must add the follow of the
                        # principal non-terminal to the follow of the symbol, with recursion
                        follow = follow.union(self.follow(principal))
                else:
                    # If the principal non-terminal is not in the subset of the symbol, then we must add the follow
                    # of the principal non-terminal to the follow of the symbol, with recursion
                    follow = follow.union(self.follow(principal))
        return follow
