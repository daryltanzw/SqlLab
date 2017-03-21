from django import forms


class TakeTestForm(forms.Form):
    
    #qids = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    #question = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    student_answer = forms.CharField(widget=forms.Textarea, label='')



