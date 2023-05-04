import time

from exceptions import *
from grammar import Grammar
from top_down_parser.top_down_parser import TopDownParser


# Test a grammar example, which we did in class
def test_grammar():
    # Create a grammar
    grammar = Grammar()
    # Add the productions
    grammar.receive_production("E -> TG")
    grammar.receive_production("G -> +TG|ε")
    grammar.receive_production("T->FJ")
    grammar.receive_production("J->*FJ|ε")
    grammar.receive_production("F->(E)|i")
    # Set the start symbol
    grammar.set_start("E")
    # Print the grammar
    print(f'{grammar}\n')

    # Proof if a grammar with ' symbol works
    grammar_2 = Grammar()
    grammar_2.receive_production("S -> AS'|bS'|cS'")
    grammar_2.receive_production("S' -> AS'|AbS'|ε")
    grammar_2.receive_production("A -> a")
    grammar_2.set_start("S")
    print(f'{grammar_2}\n')


# Test the first function
def test_first():
    # Create a grammar for the parser
    grammar = Grammar()
    grammar.receive_production("E -> TE'")
    grammar.receive_production("E' -> +TE'|ε")
    grammar.receive_production("T->FT'")
    grammar.receive_production("T'->*FT'|ε")
    grammar.receive_production("F->(E)|i")
    grammar.set_start("E")
    # Create a parser for the grammar
    parser = TopDownParser(grammar)
    # Print the first of the start symbol in this case should be {i, (}
    print(parser.first("E"))
    # Print the first of the string +TE' in this case should be {+}
    print(parser.first("+TE'"))
    # Print the first of the string E'T' in this case should be {+, *, ε}
    print(parser.first("T'E'"))
    print()

    grammar_2 = Grammar()
    grammar_2.receive_production("S -> (S)S'|()S'")
    grammar_2.receive_production("S' -> SS'|ε")
    grammar_2.set_start("S")
    parser_2 = TopDownParser(grammar_2)
    # Print the first of the start symbol in this case should be {(}
    print(parser_2.first("S"))
    # Print the first of the string ()S' in this case should be {(, ε}
    print(parser_2.first("S'"))
    print()

    grammar_3 = Grammar()
    grammar_3.receive_production("S -> (S)S'|S'")
    grammar_3.receive_production("S' -> SS'|ε")
    grammar_3.set_start("S")
    parser_3 = TopDownParser(grammar_3)
    # Print the first of the start symbol in this case should be {(, ε}
    print(parser_3.first("S"))
    # Print the first of the string ()S' in this case should be {(, ε}
    print(parser_3.first("S'"))


# Test the follow function
def test_follow():
    # Create a grammar for the parser
    grammar = Grammar()
    grammar.receive_production("E -> TE'")
    grammar.receive_production("E' -> +TE'|ε")
    grammar.receive_production("T->FT'")
    grammar.receive_production("T'->*FT'|ε")
    grammar.receive_production("F->(E)|i")
    grammar.set_start("E")
    # Create a parser for the grammar
    parser = TopDownParser(grammar)
    # Print the follow of the start symbol in this case should be {$, )} (the order is not important)
    print(f'Follow of {grammar.start}: {parser.follow(grammar.start)}')
    # Print the follow of the non-terminal E' in this case should be {$, )} (the order is not important)
    print('Follow of E\': ' + str(parser.follow("E'")))
    # Print the follow of the non-terminal T in this case should be {$, ), +} (the order is not important)
    print(f'Follow of T: {parser.follow("T")}')
    # Print the follow of the non-terminal T' in this case should be {$, ), +} (the order is not important)
    print("Follow of T': {}".format(parser.follow("T'")))
    # Print the follow of the non-terminal F in this case should be {$, ), +, *} (the order is not important)
    print(f'Follow of F: {parser.follow("F")}')
    print()

    grammar_2 = Grammar()
    grammar_2.receive_production("S' -> SS'|ε")
    grammar_2.receive_production("S -> (S)S'|()S'")
    grammar_2.set_start("S")
    parser_2 = TopDownParser(grammar_2)
    # Print the follow of the start symbol in this case should be {$, (, )} (the order is not important)
    print(f'Follow of S: {parser_2.follow("S")}')
    # Print the follow of the non-terminal S' in this case should be {$, (, )} (the order is not important)
    print(f'Follow of S\': ' + str(parser_2.follow("S'")))
    print()

    grammar_3 = Grammar()
    grammar_3.receive_production("E -> (A)")
    grammar_3.receive_production("A -> CB")
    grammar_3.receive_production("B -> ;A|ε")
    grammar_3.receive_production("C -> x|E")
    grammar_3.set_start("E")
    parser_3 = TopDownParser(grammar_3)
    # Print the follow of the start symbol in this case should be {$, ;, )} (the order is not important)
    print(f'Follow of E: {parser_3.follow("E")}')
    # Print the follow of the non-terminal A in this case should be {)} (the order is not important)
    print(f'Follow of A: ' + str(parser_3.follow("A")))
    # Print the follow of the non-terminal B in this case should be {)} (the order is not important)
    print(f'Follow of B: ' + str(parser_3.follow("B")))
    # Print the follow of the non-terminal C in this case should be {;, )} (the order is not important)
    print(f'Follow of C: ' + str(parser_3.follow("C")))
    print()

    grammar_4 = Grammar()
    grammar_4.receive_production("E -> yGH")
    grammar_4.receive_production("H -> xH|ε")
    grammar_4.receive_production("G -> A|B")
    grammar_4.receive_production("A -> ε")
    grammar_4.receive_production("V -> A|bA")
    grammar_4.receive_production("B -> bV")
    grammar_4.set_start("E")
    parser_4 = TopDownParser(grammar_4)
    # Print the follow of the start symbol in this case should be {$} (the order is not important)
    print(f'Follow of E: {parser_4.follow("E")}')
    # Print the follow of the non-terminal H in this case should be {$} (the order is not important)
    print(f'Follow of H: ' + str(parser_4.follow("H")))
    # Print the follow of the non-terminal G in this case should be {$, x} (the order is not important)
    print(f'Follow of G: ' + str(parser_4.follow("G")))
    # Print the follow of the non-terminal A in this case should be {$, x, b} (the order is not important)
    print(f'Follow of A: ' + str(parser_4.follow("A")))
    # Print the follow of the non-terminal V in this case should be {$, x, b} (the order is not important)
    print(f'Follow of V: ' + str(parser_4.follow("V")))
    # Print the follow of the non-terminal B in this case should be {$, x} (the order is not important)
    print(f'Follow of B: ' + str(parser_4.follow("B")))
    print()

    grammar_5 = Grammar()
    grammar_5.receive_production("S -> aB")
    grammar_5.receive_production("B -> bC")
    grammar_5.receive_production("C -> cS|ε")
    grammar_5.set_start("S")
    parser_5 = TopDownParser(grammar_5)
    # Print the follow of the start symbol in this case should be {$} (the order is not important)
    print(f'Follow of S: {parser_5.follow("S")}')
    # Print the follow of the non-terminal B in this case should be {$} (the order is not important)
    print(f'Follow of B: ' + str(parser_5.follow("B")))
    # Print the follow of the non-terminal C in this case should be {$} (the order is not important)
    print(f'Follow of C: ' + str(parser_5.follow("C")))


# Test the check LL(1) function
def test_check_ll1():
    # Create a grammar for the parser
    grammar = Grammar()
    grammar.receive_production("T->FT'")
    grammar.receive_production("E' -> +TE'|ε")
    grammar.receive_production("T'->*FT'|ε")
    grammar.receive_production("F->(E)|i")
    grammar.receive_production("E -> TE'")
    grammar.set_start("E")
    # Create a parser for the grammar
    parser = TopDownParser(grammar)
    # Check if the grammar is LL(1), in this case should be True
    print(f'The grammar\n{grammar}\nIs LL(1): {parser.is_ll1()}')
    print()

    grammar_2 = Grammar()
    grammar_2.receive_production("S' -> SS'|ε")
    grammar_2.receive_production("S -> (S)S'|()S'")
    grammar_2.set_start("S")
    parser_2 = TopDownParser(grammar_2)
    # Check if the grammar is LL(1), in this case should be False
    print(f'The grammar\n{grammar_2}\nIs LL(1): {parser_2.is_ll1()}')
    print()

    grammar_3 = Grammar()
    grammar_3.receive_production("E -> (A)")
    grammar_3.receive_production("A -> CB")
    grammar_3.receive_production("B -> ;A|ε")
    grammar_3.receive_production("C -> x|E")
    grammar_3.set_start("E")
    parser_3 = TopDownParser(grammar_3)
    # Check if the grammar is LL(1), in this case should be True
    print(f'The grammar\n{grammar_3}\nIs LL(1): {parser_3.is_ll1()}')
    print()

    grammar_4 = Grammar()
    grammar_4.receive_production("E -> yGH")
    grammar_4.receive_production("H -> xH|ε")
    grammar_4.receive_production("G -> A|B")
    grammar_4.receive_production("A -> ε")
    grammar_4.receive_production("V -> A|bA")
    grammar_4.receive_production("B -> bV")
    grammar_4.set_start("E")
    parser_4 = TopDownParser(grammar_4)
    # Check if the grammar is LL(1), in this case should be True
    print(f'The grammar\n{grammar_4}\nIs LL(1): {parser_4.is_ll1()}')


# Test the table function
def test_table():
    # Create a grammar for the parser
    grammar = Grammar()
    grammar.receive_production("E -> TE'")
    grammar.receive_production("E' -> +TE'|ε")
    grammar.receive_production("T->FT'")
    grammar.receive_production("T'->*FT'|ε")
    grammar.receive_production("F->(E)|i")
    grammar.set_start("E")
    # Create a parser for the grammar
    parser = TopDownParser(grammar)
    # Print the table
    # _ |     i    |      +     |      *     |      (     |      )     |      $     |
    # E | E -> TE' |            |            | E -> TE'   |            |            |
    # E'|          | E' -> +TE' |            |            | E' -> ε    | E' -> ε    |
    # T | T -> FT' |            |            | T -> FT'   |            |            |
    # T'|          | T' -> ε    | T' -> *FT' |            | T' -> ε    | T' -> ε    |
    # F |  F -> i  |            |            | F -> (E)   |            |            |
    parser.create_table()
    print(parser)

    grammar_2 = Grammar()
    grammar_2.receive_production("S -> (S)S'|()S'")
    grammar_2.receive_production("S' -> SS'|ε")
    grammar_2.set_start("S")
    parser_2 = TopDownParser(grammar_2)
    # Print the table
    # _ |        (        |      )     |      $     |
    # S | S -> (S)S'|()S' |            |            |
    # S'|   S' -> SS'|ε   | S' -> ε    | S' -> ε    |
    try:
        parser_2.create_table()
        print(parser_2)
    except AssertionError:
        print(f'The grammar\n{grammar_2}\nIs not LL(1)')
        print()

    grammar_3 = Grammar()
    grammar_3.receive_production("E -> (A)")
    grammar_3.receive_production("A -> CB")
    grammar_3.receive_production("B -> ;A|ε")
    grammar_3.receive_production("C -> x|E")
    grammar_3.set_start("E")
    parser_3 = TopDownParser(grammar_3)
    parser_3.create_table()
    print(parser_3)


# Test the parser function
def test_parser():
    # Create a grammar for the parser
    grammar = Grammar()
    grammar.receive_production("E -> TE'")
    grammar.receive_production("E' -> +TE'|ε")
    grammar.receive_production("T->FT'")
    grammar.receive_production("T'->*FT'|ε")
    grammar.receive_production("F->(E)|i")
    grammar.set_start("E")
    # Create a parser for the grammar
    parser = TopDownParser(grammar)
    # Create a table
    parser.create_table()
    # Print the parsing result of the string i+i, should be True
    print(parser.parse("i+i"))
    # Print the parsing result of the string i+i*i+, should be False
    print(parser.parse("i+i*i+"))
    # Print the parsing result of the string (i+(i*i)), should be True
    print(parser.parse("(i+(i*i))"))
    # Print the parsing result of the string (i(+(i*i))), should be False
    print(parser.parse("(i(+(i*i)))"))
    print()

    grammar_2 = Grammar()
    grammar_2.receive_production("E -> (A)")
    grammar_2.receive_production("A -> CB")
    grammar_2.receive_production("B -> ;A|ε")
    grammar_2.receive_production("C -> x|E")
    grammar_2.set_start("E")
    parser_2 = TopDownParser(grammar_2)
    parser_2.create_table()
    # Print the parsing result of the string (x;x), should be True
    print(parser_2.parse("(x;x)"))
    # Print the parsing result of the string (x;x;x), should be True
    print(parser_2.parse("(x;x;x)"))
    # Print the parsing result of the string (x;x;x;), should be False
    print(parser_2.parse("(x;x;x;)"))


# Test with a menu
def final_test(grammar: Grammar = None, parser: TopDownParser = None):
    # Create a grammar for the parser
    if grammar is None:
        grammar = Grammar()
    # Create a parser for the grammar
    if parser is None:
        parser = TopDownParser(grammar)
    try:
        # Print the menu
        option = menu()
        while True:
            # Options 1 to 8
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
                    raise GrammarNotCreatedException("The grammar hasn't been created yet")
                if grammar.start is None:
                    raise StartSymbolNotFoundException("Start symbol not found, please insert it first")
                print(grammar)
                time.sleep(5)
            elif option == 4:
                print("The grammar has been deleted successfully")
                grammar = Grammar()
                parser = TopDownParser(grammar)
                time.sleep(2)
            elif option == 5:
                if len(grammar.terminals) == 0:
                    raise GrammarNotCreatedException("The grammar hasn't been created yet")
                if grammar.start is None:
                    raise StartSymbolNotFoundException("Start symbol not found, please insert it first")
                option_5(parser)
                time.sleep(2)
            elif option == 6:
                if len(grammar.terminals) == 0:
                    raise GrammarNotCreatedException("The grammar hasn't been created yet")
                if grammar.start is None:
                    raise StartSymbolNotFoundException("Start symbol not found, please insert it first")
                option_6(parser)
                time.sleep(2)
            elif option == 7:
                if len(grammar.terminals) == 0:
                    raise GrammarNotCreatedException("The grammar hasn't been created yet")
                if grammar.start is None:
                    raise StartSymbolNotFoundException("Start symbol not found, please insert it first")
                parser.create_table()
                print(parser)
                time.sleep(5)
            elif option == 8:
                if len(grammar.terminals) == 0:
                    raise GrammarNotCreatedException("The grammar hasn't been created yet")
                if grammar.start is None:
                    raise StartSymbolNotFoundException("Start symbol not found, please insert it first")
                parser.create_table()
                option_8(parser)
                time.sleep(2)
            elif option == 9:
                print("Exiting...")
                break
            option = menu()

    except ValueError:
        print('Invalid option, please choose a number between 1 and 9')
        time.sleep(2)
        final_test(grammar, parser)
    except GrammarNotCreatedException as e:
        print(e)
        time.sleep(2)
        final_test(grammar, parser)
    except StartSymbolNotFoundException as e:
        print(e)
        time.sleep(2)
        final_test(grammar, parser)
    except SymbolNotFoundException as e:
        print(e)
        time.sleep(2)
        final_test(grammar, parser)
    except NotLL1Exception as e:
        print(e)
        print("Please insert a new grammar")
        time.sleep(3)
        final_test()


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
    except InvalidProductionException as e:
        print(e)
        time.sleep(1.5)
        option_1(grammar)
    except InvalidNonTerminalException as e:
        print(e)
        time.sleep(1.5)
        option_1(grammar)


# Option 2 of the menu
def option_2(grammar: Grammar):
    # Insert the start symbol
    start = input('Insert the start symbol: ')
    grammar.set_start(start)


# Option 5 of the menu
def option_5(parser: TopDownParser):
    try:
        symbol = input('Insert the symbol or string: ')
        print(parser.first(symbol))
    except SymbolNotFoundException as e:
        print(e)
        time.sleep(1.5)
        option_5(parser)


# Option 6 of the menu
def option_6(parser: TopDownParser):
    try:
        symbol = input('Insert the non-terminal: ')
        if symbol not in parser.grammar.non_terminals:
            raise InvalidNonTerminalException('The symbol is not a non-terminal of the grammar')
        print(parser.follow(symbol))
    except InvalidNonTerminalException as e:
        print(e)
        time.sleep(1.5)
        option_6(parser)


# Option 8 of the menu
def option_8(parser):
    try:
        string = input('Insert the string to check: ')
        for symbol in string:
            if symbol not in parser.grammar.terminals:
                raise SymbolNotFoundException('The string contains characters that are not in the grammar')
        if parser.parse(string):
            print(f'The string {string} is accepted')
        else:
            print(f'The string {string} is not accepted')
    except SymbolNotFoundException as e:
        print(e)
        time.sleep(1.5)
        option_8(parser)
    except RecursionError:
        print('This grammar generates an infinite recursion, please insert a new grammar')
        time.sleep(1.5)
        final_test()


# Menu function
def menu() -> int:
    print('Menu')
    print('1. Insert productions')
    print('2. Set start symbol')
    print('3. Print grammar')
    print('4. Delete grammar')
    print('5. Print first')
    print('6. Print follow')
    print('7. Print table')
    print('8. Parse string')
    print('9. Exit')
    option = int(input('Choose an option: '))
    if option < 1 or option > 9:
        raise ValueError('Invalid option, please choose a number between 1 and 9')
    return option
