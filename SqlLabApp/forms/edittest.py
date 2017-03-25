from django.forms import ModelForm
from SqlLabApp.models import TestForClass


class EditTestForm(ModelForm):
    class Meta:
        model = TestForClass
        fields = ['start_time', 'end_time', 'max_attempt']
