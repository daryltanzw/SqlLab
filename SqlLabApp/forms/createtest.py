from django import forms


class CreateTestForm(forms.Form):
    test_name = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Test Name'}), label='')
    start_time = forms.DateField(widget=forms.widgets.DateInput(attrs={'class': 'datepicker', 'placeholder': 'Start Date'}), label='')
    end_time = forms.DateField(widget=forms.widgets.DateInput(attrs={'class': 'datepicker', 'placeholder': 'End Date'}), label='')
    max_attempt = forms.IntegerField(widget=forms.widgets.NumberInput(
                    attrs={'placeholder': 'Number of Attempts Allowed (Leave Blank for Unlimited)'}),
                    label='', initial=None)
    q_a_file_upload = forms.FileField(label="Upload Tab Separated File ( Question <tab> Answer )")
    data_file_upload = forms.FileField(label="Upload .sql dumps")

    class Meta:
        fields = ['test_name', 'max_attempt', 'start_time', 'end_time', 'q_a_file_upload', 'data_file_upload']


