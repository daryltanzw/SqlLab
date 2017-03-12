from django import forms


class CreateTestForm(forms.Form):
    question = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Question'}), label='')
    answer = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Question'}), label='')

    class Meta:
        fields = ['question', 'answer']
