from src.fields import IntegerField, BaseField, ForeignKey
from src.query.query_creator import QueryCreator

from .abstract import ModelABC
from .exeptions import ThePrimaryKeyIsImmutable


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        fields = {'_id': IntegerField(field_name='_id', null=False, primary=True, autoincrement=True)}

        for attr_name, attr_value in list(attrs.items()):
            if isinstance(attr_value, BaseField):
                if isinstance(attr_value, ForeignKey):
                    attrs, fields = cls._set_property_for_foreign_key_field(attr_name, attr_value, attrs, fields, cls)
                else:
                    fields[attr_name] = attr_value
                    attr_value.field_name = attr_name

        attrs['_fields'] = fields
        new_cls = super().__new__(cls, name, bases, attrs)
        new_cls.query_creator = QueryCreator(new_cls)
        return new_cls

    @staticmethod
    def _set_property_for_foreign_key_field(attr_name: str, attr_value: ForeignKey, attrs: dict, fields: dict, cls: object) -> tuple:
        attrs, fields = cls._append_addional_fields_for_manage_relations(attr_name, attr_value, attrs, fields, cls)

        def getter(self, attr_name=attr_name, related_model=attr_value.related_model):
            id_field_name, model_object_field = cls._generate_additional_fields_for_relations(attr_name)
            if getattr(self, model_object_field, None) is None:
                id_value = getattr(self, id_field_name, None)
                if id_value is not None:
                    setattr(self, model_object_field, related_model.query_creator.get_one(_id=id_value).execute())
            return getattr(self, model_object_field, None)

        def setter(self, value, attr_name=attr_name, related_model=attr_value.related_model):
            if value is None:
                return None

            if not isinstance(value, related_model):
                raise TypeError(f"Expected instance of {related_model.__name__}, got {type(value).__name__}")
            id_field_name, model_object_field = cls._generate_additional_fields_for_relations(attr_name)
            setattr(self, id_field_name, value.id)
            setattr(self, model_object_field, value)

        attrs[attr_name] = property(getter, setter)
        return attrs, fields

    @staticmethod
    def _append_addional_fields_for_manage_relations(attr_name: str, attr_value: ForeignKey, attrs: dict, fields: dict, cls: object) -> tuple:
        id_field_name, model_object_field = cls._generate_additional_fields_for_relations(attr_name)

        attr_value.field_name = id_field_name
        fields[id_field_name] = attr_value
        attrs[id_field_name] = None
        attrs[model_object_field] = None

        return attrs, fields

    @staticmethod
    def _generate_additional_fields_for_relations(attr_name: str) -> tuple:
        id_field_name = f"id_{attr_name}"
        model_object_field = f"{attr_name}_object"
        return id_field_name, model_object_field


class Model(ModelABC, metaclass=ModelMeta):
    def __init__(self, **kwargs):
        for field_name, field_instance in self._fields.items():
            if field_instance.default is not None and kwargs.get(field_name) is None:
                setattr(self, field_name, field_instance.default)
            else:
                setattr(self, field_name, kwargs.get(field_name))
        for field_name, value in kwargs.items():
            if field_name not in list(self._fields.keys()):
                setattr(self, field_name, value)
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

    @classmethod
    def migrate(cls) -> QueryCreator:
        return cls.query_creator.migrate_table(**cls._fields)
