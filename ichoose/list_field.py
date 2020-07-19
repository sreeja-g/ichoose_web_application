from djongo import models
from django import forms

class ListFormField(forms.CharField):
    def to_python(self, value):
        if value is None:
            value = ""
        return value.split(",")

    def prepare_value(self, value):
        if value is None:
            value = []
        return ",".join(value)


class CustomListField(models.ListField):
    def formfield(self, **kwargs):
        return ListFormField(max_length=1000)
