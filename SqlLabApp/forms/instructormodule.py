from django import forms
from SqlLabApp.models import Class, ClassTeacherTeaches


class CreateModuleForm(forms.Form):
    class_name = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Enter New Module Code'}), label='')

    class Meta:
        model = Class
        fields = ['class_name']

    def save(self, user, commit=True):
        data = self.cleaned_data
        class_ = Class(class_name=data['class_name'])

        if commit:
            class_.save()

        class_teacher_teaches = ClassTeacherTeaches(
                teacher_email_id=user.email, classid=class_)

        if commit:
            class_teacher_teaches.save()

        return class_


