from collections import deque
from exceptions import NotLL1Exception
from grammar import Grammar
from parser import Parser
import re


# Class to handle the top-down parser of a grammar
class TopDownParser (Parser):
    def __init__(self, grammar: Grammar):
        super().__init__(grammar)
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

    # Function to join the first of a list of derivations
    def join_firsts(self, derivations):
        firsts = set()
        for derivation in derivations:
            firsts = firsts.union(self.first(derivation))
        return firsts

    # Function to check if the grammar is LL(1)
    def is_ll1(self):
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
            raise NotLL1Exception("The grammar is not LL(1)")
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
