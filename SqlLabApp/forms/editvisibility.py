from django import forms


class EditVisibilityForm(forms.Form):

    def __init__(self, dynamic_field_names, *args, **kwargs):
        super(EditVisibilityForm, self).__init__(*args, **kwargs)

        for field_name in dynamic_field_names:
            self.fields[field_name] = forms.BooleanField(label=field_name, required=False)