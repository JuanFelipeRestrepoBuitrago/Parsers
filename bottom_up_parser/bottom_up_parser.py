from collections import deque
from grammar import Grammar
from parser import Parser
import re
from exceptions import NotSLRException


# Class to handle the bottom-up parser of a grammar
class BottomUpParser(Parser):
    def __init__(self, grammar: Grammar):
        super().__init__(grammar)
        self.table = {}
        if grammar.start is None:
            self.states = []
            self.new_start_symbol = None
        else:
            self.update_sets()

    def update_sets(self):
        if self.grammar.start is not None:
            self.new_start_symbol = self.grammar.start + "\'"
            self.states = []
            length = 0
            # Add the start symbol plus a single quote to the grammar,
            # if it is already in the grammar, then add another single quote
            while length == 0:
                if self.new_start_symbol not in self.grammar.non_terminals:
                    self.states = [self.closure({f'{self.new_start_symbol}': ["." + self.grammar.start]})]
                    length = 1
                else:
                    self.new_start_symbol += "\'"
            self.initialize_states()
            self.initialize_table()

    # Function to check if a state is in the states array
    def add_state(self, state: dict):
        # If the state is not in the states set and is not empty, then add it to the states array
        if state not in self.states and state is not None:
            self.states.append(state)
            return True
        return False

    # Function to calculate the closure of a state
    def closure(self, state: dict):
        new_state = state.copy()
        pattern = re.compile(r'\.(?P<non_terminal>[A-Z]\'*)')
        # For each symbol in the state
        for symbol, productions in state.items():
            # For each production of the symbol
            for production in productions:
                # Check if the production has a dot before a non-terminal
                for match in pattern.finditer(production):
                    # Get the non-terminal after the dot
                    non_terminal = match.group("non_terminal")
                    # If the non-terminal is not in the state, then add it to the state
                    if non_terminal not in new_state:
                        new_state[non_terminal] = []
                    # For each derivation of the non-terminal
                    for derivation in self.grammar.productions[non_terminal]:
                        # If the derivation is not in the state, then add it to the state
                        if "." + derivation not in new_state[non_terminal]:
                            new_state[non_terminal].append("." + derivation)
        # If the new state is different from the old state, then call the closure function again
        if new_state != state:
            return self.closure(new_state)
        return new_state

    # Function to calculate the goto of a state
    def goto(self, state: dict, symbol: str):
        new_state = {}
        if symbol in self.grammar.non_terminals:
            pattern = "\." + symbol + "(?!\')"
        else:
            pattern = "\.[" + symbol + "]"
        # For each symbol in the state
        for non_terminal, productions in state.items():
            # For each item of the symbol
            for item in productions:
                # Check if the item has a dot before the symbol
                match = re.search(pattern, item)
                if match is not None:
                    # Get the index of the symbol in the item
                    index = item.index("." + symbol)
                    # Add the symbol to the new state
                    if non_terminal not in new_state:
                        new_state[non_terminal] = []
                    # Add the item to the new state
                    new_state[non_terminal].append(item[:index] + symbol + "." + item[index + len(symbol) + 1:])

        # If the new state is not empty, then calculate the closure of the new state
        if len(new_state) > 0:
            return self.closure(new_state)

    # Function to initialize the states array
    def initialize_states(self):
        length = len(self.states)
        # For each state in the states array
        for state in self.states:
            # For each terminal in the grammar
            for terminal in self.grammar.terminals:
                # Calculate the goto of the state with the terminal
                new_state = self.goto(state, terminal)
                # Add the new state to the states array
                self.add_state(new_state)

            # For each non-terminal in the grammar
            for non_terminal in self.grammar.non_terminals:
                # Calculate the goto of the state with the non-terminal
                new_state = self.goto(state, non_terminal)
                # Add the new state to the states array
                self.add_state(new_state)
        # If the length of the states array is different from the length before the loop, then call the function again
        if length != len(self.states):
            self.initialize_states()

    # Function to initialize the table
    def initialize_table(self):
        # Action and Goto tables
        self.table["Action"] = {}
        self.table["Goto"] = {}
        # For each state in the states array
        for i in range(len(self.states)):
            self.table["Action"][i] = {'$': None}
            self.table["Goto"][i] = {}
            # For each terminal in the grammar
            for terminal in self.grammar.terminals:
                self.table["Action"][i][terminal] = None
            # Put the values for the row
            self.action(self.states[i])
            # For each non-terminal in the grammar
            for non_terminal in self.grammar.non_terminals:
                goto = self.goto(self.states[i], non_terminal)
                # Verify if the cell is empty, otherwise there is a conflict
                if non_terminal in self.table["Goto"][i] and self.table["Goto"][i][non_terminal] is not None:
                    raise NotSLRException(f'The grammar is not SLR(1) because there is a conflict in the state'
                                          f' {self.states.index(i)} in the $ column')
                # If the goto is not empty
                if goto is not None:
                    self.table["Goto"][i][non_terminal] = self.states.index(goto)
                else:
                    self.table["Goto"][i][non_terminal] = None

    # Function to calculate the action of a state
    def action(self, state: dict):
        # For each symbol in the state
        for symbol, productions in state.items():
            # For each item of the symbol
            for production in productions:
                dot_index = production.index(".")
                # Ask if the dot is in the last position of the item
                if dot_index == len(production) - 1 or production[dot_index + 1] == "ε":
                    # If the symbol is the start symbol
                    if symbol == self.new_start_symbol:
                        # Add the accept action to the action table of the state, in the $ column
                        # just if the cell is empty, otherwise there is a conflict
                        if self.table["Action"][self.states.index(state)]["$"] is None:
                            self.table["Action"][self.states.index(state)]["$"] = "accept"
                        else:
                            raise NotSLRException(f'The grammar is not SLR(1) because there is a conflict in the state'
                                                  f' {self.states.index(state)} in the $ column')
                    else:
                        for terminal in self.follow(symbol):
                            # If the symbol is not in the action table of the state
                            if self.table["Action"][self.states.index(state)][terminal] is None:
                                # Add the symbol to the action table of the state
                                if not dot_index == len(production) - 1:
                                    action = "reduce " + symbol + "->" + production[-1]
                                else:
                                    action = "reduce " + symbol + "->" + production[:-1]
                                self.table["Action"][self.states.index(state)][terminal] = action

                            else:
                                raise NotSLRException(f'The grammar is not SLR(1) because there is a conflict in the '
                                                      f'state {self.states.index(state)} in the $ column')
                else:
                    # Get the symbol after the dot
                    next_symbol = production[dot_index + 1]
                    # If the symbol is a terminal
                    if next_symbol in self.grammar.terminals:
                        # If the symbol is not in the action table of the state
                        if self.table["Action"][self.states.index(state)][next_symbol] is None:
                            # Add the symbol to the action table of the state
                            self.table["Action"][self.states.index(state)][next_symbol] = "shift " + str(
                                self.states.index(self.goto(state, next_symbol)))
                        else:
                            raise NotSLRException(f'The grammar is not SLR(1) because there is a conflict in the state'
                                                  f' {self.states.index(state)} in the $ column')

    # Length of cells in action table
    def cell_length(self):
        max_length = 6
        # For each state in the action table
        for state_number, state in self.table["Action"].items():
            # For each terminal in the state
            for terminal, action in state.items():
                if action is not None:
                    if len(action) > max_length:
                        max_length = len(action)
        return max_length

    # Function to calculate the length of the goto table
    def goto_length(self):
        length = 0
        # For each non-terminal in the grammar
        for non_terminal in self.grammar.non_terminals:
            length += len(non_terminal)
        return length

    # Function to print the table
    def __str__(self):
        # Length of each cell of the action table
        length = self.cell_length() + 2
        states_length = len(str(len(self.states)))
        goto_length = (self.goto_length() * 2 - 1) + (self.goto_length() * states_length - self.goto_length())

        table_str = (" " * states_length) + "|"
        # Adding table headers
        terminals = list(self.grammar.terminals)
        terminals.append("$")
        non_terminals = list(self.grammar.non_terminals)

        # Header of the action table
        whitespace = " " * (((len(terminals) * length) - 6 + (len(terminals) - 1)) // 2)
        if ((len(terminals) * length) - 6 + (len(terminals) - 1)) % 2 == 0:
            table_str += whitespace + "Action" + whitespace + "|"
        else:
            table_str += whitespace + "Action" + whitespace + " |"
        # Header of the goto table
        whitespace = " " * ((goto_length - 4) // 2)
        if (goto_length - 4) % 2 == 0 or goto_length < 4:
            table_str += whitespace + "Goto" + whitespace + "|"
        else:
            table_str += whitespace + "Goto" + whitespace + " |"
        table_str += "\n" + (" " * states_length) + "|"

        # Adding terminals to the action table
        for terminal in terminals:
            whitespace = " " * ((length - len(terminal)) // 2)
            if (length - len(terminal)) % 2 == 0:
                table_str += whitespace + terminal + whitespace + "|"
            else:
                table_str += whitespace + terminal + whitespace + " |"

        # Adding non-terminals to the goto table
        for non_terminal in non_terminals:
            whitespace = " " * ((states_length - len(non_terminal)) // 2)
            if (states_length - len(non_terminal)) % 2 == 0:
                table_str += whitespace + non_terminal + whitespace + "|"
            else:
                table_str += whitespace + non_terminal + whitespace + " |"
        table_str += "\n"

        # Adding the values of the action table and the goto table
        for state_number, state in self.table["Action"].items():
            # Adding the state number and adding the whitespaces to align the table
            table_str += str(state_number) + (" " * (states_length - len(str(state_number)))) + "|"
            for terminal in terminals:
                # if the action is None we add whitespaces to align the table
                if self.table["Action"][state_number][terminal] is not None:
                    # Whitespace to align the table putting the action in the middle of the cell
                    whitespace = " " * ((length - len(self.table["Action"][state_number][terminal])) // 2)
                    if (length - len(self.table["Action"][state_number][terminal])) % 2 == 0:
                        table_str += whitespace + self.table["Action"][state_number][terminal] + whitespace + "|"
                    else:
                        table_str += whitespace + self.table["Action"][state_number][terminal] + whitespace + " |"
                else:
                    table_str += " " * length + "|"
            for s in non_terminals:
                # if the action is None we add whitespaces to align the table
                if self.table["Goto"][state_number][s] is not None:
                    # Whitespace to align the table putting the state number in the middle of the cell
                    whitespace = " " * ((states_length - len(str(self.table["Goto"][state_number][s]))) // 2)
                    if (states_length - len(str(self.table["Goto"][state_number][s]))) % 2 == 0:
                        table_str += whitespace + str(self.table["Goto"][state_number][s]) + whitespace + "|"
                    else:
                        table_str += whitespace + str(self.table["Goto"][state_number][s]) + whitespace + " |"
                else:
                    table_str += " " * states_length + "|"
            table_str += "\n"

        return table_str

    # Function to print the states
    def print_states(self):
        for i in range(len(self.states)):
            print("State " + str(i) + ":")
            for symbol, productions in self.states[i].items():
                for production in productions:
                    print(symbol + "->" + production, end=" | ")
            print()

    # Function to calculate the length of a production
    @staticmethod
    def production_length(production: str):
        non_terminal_pattern = re.compile(r"([A-Z]\'*)")
        length = 0
        # If the production is epsilon we return 0, because the length of empty string is 0
        if production == "ε":
            return 0
        # For each non-terminal in the production we add 1 to the length,
        # and we remove the non-terminal from the production
        for non_terminal in non_terminal_pattern.findall(production):
            length += 1
            production = production.replace(non_terminal, "", 1)
        # For each terminal in the production we add 1 to the length
        for _ in production:
            length += 1
        return length

    # Function to parse a string
    def parse(self, string: str):
        action_pattern = re.compile(
            r"(?P<Action>shift|reduce) ((?P<non_terminal>[A-Z]\'*)\s?->\s?(?P<production>.+)|(?P<state>\d+))")
        # Stack of states and adding the first state
        stack = deque()
        stack.append(0)
        # Adding the dollar sign to the end of the string
        string += "$"
        # Index of the string
        index = 0
        while True:
            state = stack[-1]
            # State action
            action = self.table["Action"][state][string[index]]
            # If the action is None we return False
            if action is None:
                return False
            elif action == "accept":
                return True
            else:
                action_match = action_pattern.match(action)
                # If the action is shift we add the state to the stack, and we move to the next symbol
                if action_match.group("Action") == "shift":
                    stack.append(int(action_match.group("state")))
                    index += 1
                # If the action is reduce we add the production to the stack
                elif action_match.group("Action") == "reduce":
                    # We remove the symbols from the stack
                    for _ in range(self.production_length(action_match.group("production"))):
                        stack.pop()
                    # We add the state to the stack
                    stack.append(self.table["Goto"][stack[-1]][action_match.group("non_terminal")])
