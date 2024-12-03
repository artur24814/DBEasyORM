from .abstract import FieldABC


class BaseField(FieldABC):
    def __init__(self, field_type, max_length=500, null=True, primary=False):
        self.field_type = field_type
        self.max_length = max_length
        self.null = null
        self.primary = primary

    def __repr__(self):
        constraints = []
        if self.max_length:
            constraints.append(f"max_length={self.max_length}")
        if self.null:
            constraints.append("null=True")
        return f"<Field type={self.field_type} {' '.join(constraints)}>"

    def get_sql(self):
        pass
