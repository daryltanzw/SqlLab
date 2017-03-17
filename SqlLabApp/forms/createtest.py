from django import forms


class CreateTestForm(forms.Form):
    test_name = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Test Name'}), label='')
    q_a_file_upload = forms.FileField(label="upload tab separated file of format( Question <tab> Answer )")
    data_file_upload = forms.FileField(label="upload .sql dumps")
    max_attempt = forms.IntegerField(widget=forms.widgets.NumberInput(
                    attrs={'placeholder': 'Number of Attempts Allowed. Leave Blank for Unlimited'}),
                    label='', initial=None)
    # start_time = forms.DateTimeField(widget=forms.widgets.DateTimeInput(format=['%Y-%m-%d %H:%M']))
    # end_time = forms.DateTimeField(widget=forms.widgets.DateTimeInput(format=['%Y-%m-%d %H:%M']))

    class Meta:
        fields = ['test_name', 'q_a_file_upload', 'data_file_upload', 'max_attempt']


