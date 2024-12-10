class TheInstanceDoesNotExistExeption(Exception):
    def __init__(self, message="The instance does not exist", code=None, instance_class=None):
        self.message = message
        self.code = code
        self.instance_class = instance_class
        super().__init__(self.message)

    def __str__(self):
        if self.code:
            return f"[Error {self.code}]: {self.message}"
        if self.instance_class:
            return f"The instance of {self.instance_class} does not exist"
        return self.message


class TheMultipleResultsExeption(Exception):
    def __init__(self, message="Expected one result, received many", code=None, instance_class=None):
        self.message = message
        self.code = code
        self.instance_class = instance_class
        super().__init__(self.message)

    def __str__(self):
        if self.code:
            return f"[Error {self.code}]: {self.message}"
        if self.instance_class:
            return f"Expected one result of {self.instance_class}, received many"
        return self.message
