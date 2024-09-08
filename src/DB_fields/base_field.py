from .abstract import FieldABC


class BaseField(FieldABC):
    def __init__(self, field_type, null=True, primary=False):
        self.field_type = field_type
        self.null = null
        self.primary = primary

    def __repr__(self):
        return f"<Field type={self.field_type}>"
