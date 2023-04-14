import re
import time
from grammar import Grammar
from bottom_up_parser.parser import Parser


def test_closure():
    # Create the grammar
    grammar = Grammar()
    grammar.receive_production("E -> E+T")
    grammar.receive_production("E -> T")
    grammar.receive_production("T -> T*F")
    grammar.receive_production("T -> F")
    grammar.receive_production("F -> (E)")
    grammar.receive_production("F -> i")
    grammar.set_start("E")
    parser = Parser(grammar)
    # Print the first state, which is the closure of the start symbol
    print(parser.states)


# Function to test the goto function
def test_goto():
    # Create the grammar
    grammar = Grammar()
    grammar.receive_production("E -> E+T")
    grammar.receive_production("E -> T")
    grammar.receive_production("T -> T*F")
    grammar.receive_production("T -> F")
    grammar.receive_production("F -> (E)")
    grammar.receive_production("F -> i")
    grammar.set_start("E")
    parser = Parser(grammar)
    # Print the first state, which is the closure of the start symbol
    print(parser.states)
    # Print the goto of the first state with the symbol E
    print('GOTO of state 0 with symbol E: ', parser.goto(parser.states[0], 'E'))
    # Print the goto of the first state with the symbol T
    print('GOTO of state 0 with symbol T: ', parser.goto(parser.states[0], 'T'))
    # Print the goto of the first state with the symbol F
    print('GOTO of state 0 with symbol F: ', parser.goto(parser.states[0], 'F'))
    # Print the goto of the first state with the symbol i
    print('GOTO of state 0 with symbol i: ', parser.goto(parser.states[0], 'i'))
    # Print the goto of the first state with the symbol +
    print('GOTO of state 0 with symbol +: ', parser.goto(parser.states[0], '+'))
    # Print the goto of the first state with the symbol *
    print('GOTO of state 0 with symbol *: ', parser.goto(parser.states[0], '*'))
    # Print the goto of the first state with the symbol (
    print('GOTO of state 0 with symbol (: ', parser.goto(parser.states[0], '('))
    # Print the goto of the first state with the symbol )
    print('GOTO of state 0 with symbol ): ', parser.goto(parser.states[0], ')'))


# Function to test the states initialization
def test_states():
    # Create the grammar
    grammar = Grammar()
    grammar.receive_production("E -> E+T")
    grammar.receive_production("E -> T")
    grammar.receive_production("T -> T*F")
    grammar.receive_production("T -> F")
    grammar.receive_production("F -> (E)")
    grammar.receive_production("F -> i")
    grammar.set_start("E")
    parser = Parser(grammar)
    parser.initialize_states()
    # Print the states
    for state in parser.states:
        print(state)
        print('----------------------------------------')
    print(len(parser.states))


# Function to test the action function
def test_action():
    # Create the grammar
    grammar = Grammar()
    grammar.receive_production("E -> E+T")
    grammar.receive_production("E -> T")
    grammar.receive_production("T -> T*F")
    grammar.receive_production("T -> F")
    grammar.receive_production("F -> (E)")
    grammar.receive_production("F -> i")
    grammar.set_start("E")
    parser = Parser(grammar)
    parser.initialize_states()
    parser.initialize_table()
    # Print Action of state {E: [E.], E: [E.+T]}
    index = parser.states.index({"E'": ['E.'], 'E': ['E.+T']})
    parser.action({"E'": ['E.'], 'E': ['E.+T']})
    print('ACTION of state {E: [E.], E: [E.+T]} with symbol : ', parser.table["Action"][index])


# Function to test the print_table function
def test_print_table():
    # Create the grammar
    grammar = Grammar()
    grammar.receive_production("E -> E+T")
    grammar.receive_production("E -> T")
    grammar.receive_production("T -> T*F")
    grammar.receive_production("T -> F")
    grammar.receive_production("F -> (E)")
    grammar.receive_production("F -> i")
    grammar.set_start("E")
    parser = Parser(grammar)
    parser.initialize_states()
    parser.initialize_table()
    print(parser)
    parser.print_states()


# Function to test the parser
def test_parser():
    # Create the grammar
    grammar = Grammar()
    grammar.receive_production("E -> E+T")
    grammar.receive_production("E -> T")
    grammar.receive_production("T -> T*F")
    grammar.receive_production("T -> F")
    grammar.receive_production("F -> (E)")
    grammar.receive_production("F -> i")
    grammar.set_start("E")
    parser = Parser(grammar)
    parser.initialize_states()
    parser.initialize_table()
    # Parse the string i+i, should return True
    print(parser.parse("i+i"))
    # Parse the string (i+i), should return True
    print(parser.parse("(i+i)"))
    # Parse the string (i+i)*i, should return True
    print(parser.parse("(i+i)*i"))
    # Parse the string (i+i)*+i, should return False
    print(parser.parse("(i+i)*+i"))


# Function with the final test
def test_final(grammar: Grammar = None, parser: Parser = None):
    if grammar is None:
        grammar = Grammar()
    if parser is None:
        parser = Parser(grammar)
    # Print the menu
    try:
        option = menu()
        while True:
            if option == 1:
                option_1(grammar)
                print("Productions inserted successfully")
                parser.update_sets()
                time.sleep(2)
            elif option == 2:
                option_2(grammar)
                parser.update_sets()
                print("Start symbol inserted successfully")
                time.sleep(2)
            elif option == 3:
                if len(grammar.terminals) == 0:
                    raise NotImplementedError("The grammar hasn't been created yet")
                if grammar.start is None:
                    raise TypeError("Start symbol not found, please insert it first")
                print(grammar)
                time.sleep(5)
            elif option == 4:
                if len(grammar.terminals) == 0:
                    raise NotImplementedError("The grammar hasn't been created yet")
                if grammar.start is None:
                    raise TypeError("Start symbol not found, please insert it first")
                option_4(grammar, parser)
                time.sleep(5)
            elif option == 5:
                if len(grammar.terminals) == 0:
                    raise NotImplementedError("The grammar hasn't been created yet")
                if grammar.start is None:
                    raise TypeError("Start symbol not found, please insert it first")
                option_5(grammar, parser)
                time.sleep(5)
            elif option == 6:
                if len(grammar.terminals) == 0:
                    raise NotImplementedError("The grammar hasn't been created yet")
                if grammar.start is None:
                    raise TypeError("Start symbol not found, please insert it first")
                parser.print_states()
                time.sleep(5)
            elif option == 7:
                if len(grammar.terminals) == 0:
                    raise NotImplementedError("The grammar hasn't been created yet")
                if grammar.start is None:
                    raise TypeError("Start symbol not found, please insert it first")
                print(parser)
                time.sleep(5)
            elif option == 8:
                if len(grammar.terminals) == 0:
                    raise NotImplementedError("The grammar hasn't been created yet")
                if grammar.start is None:
                    raise TypeError("Start symbol not found, please insert it first")
                option_8(grammar, parser)
                time.sleep(5)
            elif option == 9:
                print('Exiting program...')
                break
            option = menu()
    except ValueError:
        print('Invalid option, please choose a number between 1 and 9')
        time.sleep(2)
        test_final(grammar, parser)
    except NotImplementedError as e:
        print(e)
        time.sleep(2)
        test_final(grammar, parser)
    except TypeError as e:
        print(e)
        time.sleep(2)
        test_final(grammar, parser)
    except SyntaxError as e:
        print(e)
        time.sleep(2)
        test_final(grammar, parser)


# Menu function
def menu():
    print('Menu')
    print('1. Insert productions')
    print('2. Set start symbol')
    print('3. Print grammar')
    print('4. Print closure')
    print('5. Print goto')
    print('6. Print states')
    print('7. Print table')
    print('8. Parse string')
    print('9. Exit')
    print('----------------------------------------')
    option = int(input('Choose an option: '))
    if option < 1 or option > 9:
        raise ValueError('Invalid option, please choose a number between 1 and 9')
    return option


# Option 1 of the menu
def option_1(grammar: Grammar):
    try:
        # Insert the number of productions
        number = int(input('Insert the number of productions you want to insert: '))
        # Check if the number is greater than 0
        if number < 1:
            raise ValueError()
        # Insert the productions
        for i in range(number):
            production = input('Insert the production: ')
            grammar.receive_production(production)
    except ValueError:
        print('Invalid option, the number of productions must be an integer greater than 0')
        time.sleep(1)
        option_1(grammar)
    except SyntaxError as e:
        print(e)
        time.sleep(1.5)
        option_1(grammar)


# Option 2 of the menu
def option_2(grammar: Grammar):
    try:
        # Insert the start symbol
        start = input('Insert the start symbol: ')
        grammar.set_start(start)
    except SyntaxError as e:
        print(e)
        time.sleep(1.5)
        option_2(grammar)


def print_closure(state: dict):
    print('Closure: ')
    for symbol, derivations in state.items():
        for derivation in derivations:
            print(symbol + ' -> ' + derivation)


# Option 4 of the menu
def option_4(grammar: Grammar, parser: Parser):
    try:
        pattern = re.compile(r'\s*(?P<Symbol>[A-Z]\'*)\s?->\s?(?P<Derivations>.+)')  # Regex to check the productions
        state = dict()
        number_production = int(input('Insert the number of the production you want to see the closure: '))
        if number_production < 1:
            raise ValueError()
        for _ in range(number_production):
            production = input('Insert the production: ')
            match = pattern.match(production)
            if match is None:
                raise SyntaxError('Invalid production, it must be in the form: A -> Ba')
            symbol = match.group('Symbol')
            derivations = match.group('Derivations').split('|')
            if symbol not in state:
                state[symbol] = []
            for derivation in derivations:
                if derivation not in state[symbol]:
                    state[symbol].append(derivation)
        print_closure(parser.closure(state))
    except ValueError:
        print('Invalid option, the number of the production must be an integer greater than 0')
        time.sleep(1)
        option_4(grammar, parser)
    except SyntaxError as e:
        print(e)
        time.sleep(1.5)
        option_4(grammar, parser)


# Option 5 of the menu
def option_5(grammar: Grammar, parser: Parser):
    try:
        state_number = int(input(f'Insert the number of the state you want to see the goto (From 0 to '
                                 f'{len(parser.states) - 1}): '))
        if state_number < 0 or state_number > len(parser.states):
            raise ValueError()
        symbol = input('Insert the symbol: ')
        if symbol not in grammar.terminals and symbol not in grammar.non_terminals:
            raise SyntaxError('Invalid symbol, it must be a terminal or a non-terminal')
        index = parser.states.index(parser.goto(parser.states[state_number], symbol))
        print('Goto of the state ' + str(state_number) + ' with the symbol ' + symbol + ': ' + str(index))
        print(f'State {index}: {parser.states[index]}')

    except ValueError:
        print('Invalid option, the number of the state must be an integer between 0 and the number of states')
        time.sleep(1)
        option_5(grammar, parser)
    except SyntaxError as e:
        print(e)
        time.sleep(1.5)
        option_5(grammar, parser)


# Option 8 of the menu
def option_8(grammar: Grammar, parser: Parser):
    try:
        string = input('Insert the string to check: ')
        for symbol in string:
            if symbol not in parser.grammar.terminals:
                raise ZeroDivisionError('The string contains characters that are not in the grammar')
        if parser.parse(string):
            print(f'The string {string} is accepted')
        else:
            print(f'The string {string} is not accepted')
    except ZeroDivisionError as e:
        print(e)
        time.sleep(1.5)
        option_8(grammar, parser)
    except RecursionError:
        print('This grammar generates an infinite recursion, please insert a new grammar')
        time.sleep(1.5)
        test_final()
