class UnconfirmedAction(Exception):
    def __init__(self, message="The action was interrupted", code=None):
        self.message = message
        self.code = code
        super().__init__(self.message)

    def __str__(self):
        if self.code:
            return f"[Error {self.code}]: {self.message}"
        return self.message
