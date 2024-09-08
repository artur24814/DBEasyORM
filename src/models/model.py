from .abstract import ModelABC
from src.query_creator.query_creator import QueryCreator
from .exeptions import ThePrimaryKeyIsImmutable
from src.DB_fields.base_field import BaseField


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        fields = {}

        # Loop through class attributes and find instances of BaseField
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, BaseField):
                fields[attr_name] = attr_value

        attrs['_fields'] = fields
        new_cls = super().__new__(cls, name, bases, attrs)
        new_cls.query_creator = QueryCreator(new_cls)
        return new_cls


class Model(ModelABC, metaclass=ModelMeta):

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if self._id != -1:
            raise ThePrimaryKeyIsImmutable()
        self._id = value

    def save(self):
        pass

    def delete(self):
        pass
