from src.fields import IntegerField, BaseField
from src.query.query_creator import QueryCreator

from .abstract import ModelABC
from .exeptions import ThePrimaryKeyIsImmutable


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        fields = {'_id': IntegerField(null=False, primary=True, autoincrement=True)}

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
        for field_name, field_instance in self._fields.items():
            field_instance.field_name = field_name
            setattr(self, field_name, kwargs.get(field_name))
        self._id = kwargs.get('_id', -1)

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value) -> None:
        if self._id != -1:
            raise ThePrimaryKeyIsImmutable()
        self._id = value

    @property
    def _dict_fields(self) -> dict:
        return {field_name: getattr(self, field_name, None) for field_name in self._fields.keys() if field_name != "_id"}

    def save(self) -> QueryCreator:
        for field_name, field_instance in self._fields.items():
            value = getattr(self, field_name, None)
            field_instance.validate(value)

        if self.id == -1:
            return self.query_creator.create(**self._dict_fields)
        return self.query_creator.update(where=dict(_id=self.id), **self._dict_fields)

    def delete(self) -> QueryCreator:
        return self.query_creator.delete(where=dict(_id=self.id))
