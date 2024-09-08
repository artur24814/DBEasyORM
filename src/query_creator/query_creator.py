from .abstract import QueryCreatorABC


class QueryCreator(QueryCreatorABC):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.sql = ''
        self.many = False

    def get_table_name(self):
        return self.get_class_name().__name__.upper()

    def get_class_name(self):
        if isinstance(self.model, type):
            return self.model
        return self.model.__class__
