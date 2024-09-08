class ThePrimaryKeyIsImmutable(Exception):
    def __init__(self, message="The primary key is immutable", code=None):
        self.message = message
        self.code = code
        super().__init__(self.message)

    def __str__(self):
        if self.code:
            return f"[Error {self.code}]: {self.message}"
        return self.message
