from dbeasyorm.query.query_creator import QueryCreatorABC


class ModelABC:
    def save(self) -> QueryCreatorABC:
        ...

    def delete(self) -> QueryCreatorABC:
        ...
