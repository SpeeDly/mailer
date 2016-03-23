from django.db import models
from django.core import validators


class EmailListField(models.CharField):

    class EmailListValidator(validators.EmailValidator):
        def __call__(self, value):
            for email in value:
                super(EmailListField.EmailListValidator, self).__call__(email)

    class Presentation(list):

        def __str__(self):
            return ",".join(self)

    default_validators = [EmailListValidator()]

    def get_db_prep_value(self, value, *args, **kwargs):
        if not value:
            return
        return ','.join(unicode(s) for s in value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value

        return self.Presentation([address.strip() for address in value.split(',')])

    def to_python(self, value):
        if isinstance(value, self.Presentation):
            return value

        if value is None:
            return value

        return self.Presentation([address.strip() for address in value.split(',')])
