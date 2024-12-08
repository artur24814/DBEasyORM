from src.fields.abstract import BaseField
from src.query.query_creator import QueryCreator

from .abstract import ModelABC
from .exeptions import ThePrimaryKeyIsImmutable


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
    def __init__(self, **kwargs):
        self._id = -1
        for field_name in self._fields:
            setattr(self, field_name, kwargs.get(field_name))

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value) -> None:
        if self._id != -1:
            raise ThePrimaryKeyIsImmutable()
        self._id = value

    def save(self) -> QueryCreator:
        for field_name, field_instance in self._fields.items():
            value = getattr(self, field_name, None)
            field_instance.validate(value)

        if self.id != -1:
            return self.query_creator.create(**self._fields)

        return self.query_creator.update(**self._fields)

    def delete(self) -> QueryCreator:
        return self.query_creator.delete(self.id)
