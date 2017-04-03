from django import forms


class CreateModuleForm(forms.Form):
    class_name = forms.CharField(widget=forms.widgets.TextInput(attrs={}), label='Module Name')
    semester = forms.CharField(widget=forms.widgets.TextInput(attrs={}), label='Semester')
    facilitators = forms.CharField(widget=forms.widgets.TextInput(attrs={}), label='Facilitators')

    class Meta:
        fields = ['class_name', 'semester', 'facilitators']