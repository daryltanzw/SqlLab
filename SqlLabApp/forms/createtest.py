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

    # def clean(self):
    #     start_time = self.data.get('start_time')
    #     end_time = self.data.get('end_time')
    #
    #     if start_time < datetime.date.today() | end_time < datetime.date.today():
    #         raise forms.ValidationError("The date cannot be in the past!")
    #
    #     if start_time >= end_time :
    #         raise forms.ValidationError("Start Date should be before End Date!")
    #
    #     return start_time
