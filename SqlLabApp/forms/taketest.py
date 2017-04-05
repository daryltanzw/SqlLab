from django import forms


class TakeTestForm(forms.Form):
    
    student_answer = forms.CharField(widget=forms.Textarea, label='', required=True)



