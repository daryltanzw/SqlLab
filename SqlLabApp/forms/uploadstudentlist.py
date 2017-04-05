from django.forms import forms


class TeacherManageModule(forms.Form):
    student_list_file_upload = forms.FileField(label="Upload List of Students .txt")

    class Meta:
        fields = ["student_list_file_upload"]
