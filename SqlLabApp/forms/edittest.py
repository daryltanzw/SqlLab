from django import forms
from django.forms import ModelForm
from SqlLabApp.models import TestForClass


class EditTestForm(ModelForm, forms.Form):
    class Meta:
        model = TestForClass
        fields = ['start_time', 'end_time', 'max_attempt']

    def __init__(self, dynamic_field_names, *args, **kwargs):
        super(EditTestForm, self).__init__(*args, **kwargs)

        for row in dynamic_field_names:
            field_name = row['name']
            visi = row['visibility']
            self.fields[field_name] = forms.BooleanField(label=field_name.title(), required=False, label_suffix='', initial=visi)
