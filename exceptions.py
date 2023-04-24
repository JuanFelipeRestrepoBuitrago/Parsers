# Exception raised when the grammar is not SLR, used in bottom-up parser
class NotSLRException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# Exception raised when the grammar is not LL(1), used in top-down parser
class NotLL1Exception(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)