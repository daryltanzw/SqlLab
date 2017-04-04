import datetime
import time
from django import forms


class CreateTestForm(forms.Form):
    test_name = forms.CharField(widget=forms.widgets.TextInput(attrs={}), label='Test Name')
    start_time = forms.CharField(widget=forms.widgets.DateTimeInput(attrs={}), label='Start Date')
    end_time = forms.CharField(widget=forms.widgets.DateTimeInput(attrs={}), label='End Date')
    max_attempt = forms.IntegerField(widget=forms.widgets.NumberInput(
                    attrs={'min': '0'}),
                    label='Number of Attempts (Leave Blank for Unlimited)', initial=None, required=False)
    q_a_file_upload = forms.FileField(label="Upload Tab Separated File (.txt, .tsv)")
    data_file_upload = forms.FileField(label="Upload .sql dump")

    class Meta:
        fields = ['test_name','start_time', 'end_time', 'max_attempt', 'q_a_file_upload', 'data_file_upload']

    def clean(self):
        start_time = self.data.get('start_time')
        end_time = self.data.get('end_time')
        current_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

        if start_time <= current_time:
            raise forms.ValidationError("Start date cannot be in the past.")

        if end_time <= current_time:
            raise forms.ValidationError("End date cannot be in the past.")

        if start_time >= end_time:
            raise forms.ValidationError("Start date should be before end date.")

        return start_time
