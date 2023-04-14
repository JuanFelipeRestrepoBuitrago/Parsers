from collections import deque

from grammar import Grammar
import re


# Class to handle the top-down parser of a grammar
class Parser:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.table = [[None for _ in range(len(grammar.terminals) + 1)] for _ in range(
            len(grammar.non_terminals))]
        self.rows = list(grammar.non_terminals)
        self.columns = list(grammar.terminals.union({'$'}))

    # Function to update the rows and columns of the table
    def update_sets(self):
        self.rows = list(self.grammar.non_terminals)
        self.columns = list(self.grammar.terminals.union({'$'}))
        self.table = [[None for _ in range(len(self.grammar.terminals) + 1)] for _ in range(
            len(self.grammar.non_terminals))]

    # Function to check if the table is filled
    def is_filled(self):
        for row in self.table:
            for element in row:
                if element is not None:
                    return True
        return False

    # Function to calculate the first of a symbol or string
    def first(self, symbol: str):
        first = set()
        if len(symbol) == 1 or symbol in self.grammar.non_terminals:
            # Check if the symbol is in the grammar
            if (
                    symbol not in self.grammar.terminals
                    and symbol not in self.grammar.non_terminals
                    and symbol != "ε"
            ):
                raise SyntaxError("Symbol {} is not in the grammar".format(symbol))
            else:
                # If the symbol is a terminal or epsilon, then the first is set containing the symbol itself
                if symbol in self.grammar.terminals or symbol == "ε":
                    first.add(symbol)
                # If the symbol is a non-terminal
                else:
                    # For each derivation of the symbol
                    for derivation in self.grammar.productions[symbol]:
                        # Check each character of the derivation
                        first = self.check_each_character(symbol, derivation, first)
        else:
            # Check each character of the string, in case the symbol is a string
            first = self.check_each_character(symbol, symbol, first)
        return first

    # Function to check each character of a derivation in the first function
    def check_each_character(self, symbol: str, string: str, first: set) -> set:
        pattern = re.compile(r"[A-Z]\'+")
        element = 0
        while element < len(string):
            # Check if the current character is a non-terminal with a prime (A'),
            # in this case, we need to check the first of the non-terminal with the prime (A')
            # and add 1 to the element to check the next character's first of the string
            if element <= len(string) - 2 and pattern.match(string[element] + string[element + 1]):
                if string[element] + string[element + 1] == symbol:
                    return first
                first_of_element = self.first(string[element] + string[element + 1])
                element += 1
            else:
                if string[element] == symbol:
                    return first
                first_of_element = self.first(string[element])

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
                # Check if the symbol is in the derivation, and it does not have a prime (A')
                # if it has a prime, then it is not the same symbol, for example, A' != A and A'' != A'
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

    # Function to join the first of a list of derivations
    def join_firsts(self, derivations):
        firsts = set()
        for derivation in derivations:
            firsts = firsts.union(self.first(derivation))
        return firsts

    # Function to check if the grammar is LL(1)
    def is_ll1(self):
        # if self.check_left_recursion():
        #     return False
        for non_terminal in self.grammar.productions.keys():
            # If the non-terminal has more than one derivation
            if len(self.grammar.productions[non_terminal]) > 1:
                # Check the intersection of the first of every derivation
                for derivation in self.grammar.productions[non_terminal]:
                    # Remove the derivation from the list of derivations of the non-terminal temporarily
                    self.grammar.productions[non_terminal].remove(derivation)
                    # If the first of the derivation contains a terminal that is also in the first of the others
                    if len(self.join_firsts(
                            self.grammar.productions[non_terminal]).intersection(self.first(derivation))) > 0:
                        # Add the derivation to the list of derivations of the non-terminal again
                        self.grammar.productions[non_terminal].append(derivation)
                        return False
                    # Add the derivation to the list of derivations of the non-terminal again
                    self.grammar.productions[non_terminal].append(derivation)

                # Check if a derivation contains epsilon
                for derivation in self.grammar.productions[non_terminal]:
                    if self.first(derivation).__contains__("ε"):
                        # Remove the derivation from the list of derivations of the non-terminal temporarily
                        self.grammar.productions[non_terminal].remove(derivation)
                        # If the follow of the non-terminal contains a terminal that is also in the first of the
                        # derivation, then the grammar is not LL(1)
                        if len(self.follow(non_terminal).intersection(self.join_firsts(
                                self.grammar.productions[non_terminal]))) > 0:
                            # Add the derivation to the list of derivations of the non-terminal again
                            self.grammar.productions[non_terminal].append(derivation)
                            return False
                        # Add the derivation to the list of derivations of the non-terminal again
                        self.grammar.productions[non_terminal].append(derivation)
        return True

    # Function to check if the grammar has left recursion
    def check_left_recursion(self):
        # Loop through the keys of the productions
        keys = list(self.grammar.productions.keys())
        # Loop through the keys of the productions
        for i in range(len(keys)):
            # Loop through all the keys before the current key
            for j in range(i):
                # Loop through the derivations of the current key
                for derivation in self.grammar.productions[keys[i]]:
                    # If the j key is in the start of the derivation, then the grammar has left recursion
                    if derivation.startswith(keys[j]):
                        return True
            # Check for immediate left recursion
            for derivation in self.grammar.productions[keys[i]]:
                if derivation.startswith(keys[i]):
                    return True
        return False

    # Function to insert a value in the parsing table
    def insert_into_table(self, row, column, value):
        # If the cell is not empty, then add the value to the cell with a '|' separator
        if self.table[self.rows.index(row)][self.columns.index(column)] is not None:
            if value not in str(self.table[self.rows.index(row)][self.columns.index(column)]).split('|'):
                self.table[self.rows.index(row)][self.columns.index(column)] += '|' + value
        else:
            self.table[self.rows.index(row)][self.columns.index(column)] = value

    # Function to create the parsing table
    def create_table(self):
        if not self.is_ll1():
            raise AssertionError()
        # Go through every production of the grammar
        for non_terminal, derivations in self.grammar.productions.items():
            # For each derivation of the non-terminal
            for derivation in derivations:
                # First of the derivation
                first = self.first(derivation)
                # If the first of the derivation contains epsilon, then add the terminals in the follow
                # of the non-terminal to the table
                if "ε" in first:
                    first.remove("ε")
                    follow = self.follow(non_terminal)
                    # Add every terminal in the follow of the non-terminal to the table
                    for terminal in follow:
                        self.insert_into_table(non_terminal, terminal, derivation)
                # Add every terminal in the first of the derivation to the table
                for terminal in first:
                    self.insert_into_table(non_terminal, terminal, derivation)

    # Function to parse a string using a LL(1) grammar
    def parse(self, string: str):
        # If the table is not filled, then fill it
        if not self.is_filled():
            self.create_table()

        # Add $ to the end of the string
        string += "$"
        # Stack to store the symbols
        stack = deque()
        # Add $ to the stack
        stack.append("$")
        # Add the start symbol to the stack
        stack.append(self.grammar.start)
        # Index of the current character in the string
        index = 0
        # While the stack is not empty
        while stack:
            # Get the top of the stack
            top = stack.pop()
            # If the top of the stack is a terminal
            if top in self.columns:
                # If the top of the stack is the current character
                if top == string[index]:
                    # Advance the index
                    index += 1
                else:
                    # Error
                    return False
            else:
                # If the top of the stack is a non-terminal
                # Get the values from the table
                value = self.table[self.rows.index(top)][self.columns.index(string[index])]
                # If the values is None, then the string is not accepted
                if value is None:
                    return False
                pattern = re.compile(r"([A-Z]\'*|.)")
                # Get the symbols in the derivation
                symbols = pattern.findall(value)
                symbols.reverse()
                for symbol in symbols:
                    # If the symbol is not epsilon, then add it to the stack
                    if symbol != "ε":
                        stack.append(symbol)

        return True

    # Function to check the longest element in the table to print it uniformly
    def check_longest_table_element(self):
        # Case the longest is None
        longest_element = 4
        for i in range(len(self.table)):
            for j in range(len(self.table[i])):
                # If the cell is not empty
                if self.table[i][j] is not None:
                    # If the length of the cell is bigger than the longest, then update the longest
                    # (we add 4 and the length of the row because we add the row name and " -> "
                    if len(str(self.table[i][j])) + 4 + len(self.rows[i]) > longest_element:
                        longest_element = len(str(self.table[i][j])) + 4 + len(self.rows[i])
        return longest_element

    # Function to check the length of the longest non-terminal
    def check_length_of_longest_non_terminal(self):
        longest_element = 0
        for non_terminal in self.rows:
            if len(non_terminal) > longest_element:
                longest_element = len(non_terminal)
        return longest_element

    # Function to print the parsing table in case
    def __str__(self):
        # Length of the longest element in the table plus 2 whitespaces
        number_characters = self.check_longest_table_element() + 2
        # Length of the longest non-terminal
        non_terminal_whitespaces = self.check_length_of_longest_non_terminal()
        string = "Table:\n"

        # Print the header of the table
        header = ' ' * non_terminal_whitespaces + "|"
        # For each terminal
        for column in self.columns:
            # Look for the whitespaces to add to the start and end of the terminal
            whitespace = ' ' * ((number_characters - len(column)) // 2)
            # If the length of the terminal is odd, then add an extra whitespace to the end
            if (number_characters - len(column)) % 2 != 0:
                header += whitespace + column + whitespace + ' ' + "|"
            else:
                header += whitespace + column + whitespace + "|"

        string += header + "\n"

        # Print the rows of the table
        for i in range(len(self.table)):
            # If the row has only one character, then add the necessary whitespaces
            if len(self.rows[i]) == non_terminal_whitespaces:
                string += self.rows[i] + "|"
            else:
                string += self.rows[i] + ' ' * (non_terminal_whitespaces - len(self.rows[i])) + '|'
            # For each cell in the row
            for j in range(len(self.table[i])):
                # If the cell is empty, then add the necessary whitespaces
                if self.table[i][j] is None:
                    string += ' ' * number_characters + "|"
                else:
                    # Look for the whitespaces to add to the start and end of the cell
                    whitespace = ' ' * ((number_characters - len(str(self.table[i][j])) - 4 - len(self.rows[i])) // 2)
                    # If the number of whitespaces is odd, then add one more whitespace to the start
                    if (number_characters - len(str(self.table[i][j])) - 4 - len(self.rows[i])) % 2 != 0:
                        string += whitespace + f'{self.rows[i]} -> ' + str(self.table[i][j]) + whitespace + ' ' + "|"
                    else:
                        string += whitespace + f'{self.rows[i]} -> ' + str(self.table[i][j]) + whitespace + "|"

            string += "\n"

        return string
