from django.forms import ModelForm
from SqlLabApp.models import Class


class EditModuleForm(ModelForm):
    class Meta:
        model = Class
        fields = ['class_name', 'semester', 'facilitators']
