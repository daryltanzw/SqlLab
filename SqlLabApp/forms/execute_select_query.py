from django import forms


class ExecuteSelectQueryForm(forms.Form):

    query = forms.CharField(widget=forms.Textarea, label='')
