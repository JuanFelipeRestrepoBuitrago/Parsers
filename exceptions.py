# Exception raised when the grammar is not SLR, used in bottom-up parser
class NotLR0Exception(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# Exception raised when the grammar is not LL(1), used in top-down parser
class NotLL1Exception(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# Exception raised when the grammar hasn't been created
class GrammarNotCreatedException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# Exception raised when the grammar hasn't a start symbol
class StartSymbolNotFoundException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# Exception raised when a symbol is not in the grammar
class SymbolNotFoundException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# Exception raised when a production is not valid
class InvalidProductionException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# Exception raised when a non-terminal is not valid
class InvalidNonTerminalException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
