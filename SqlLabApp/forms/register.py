from django import forms
from SqlLabApp.models import User, UserRole


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}), label='')
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Full Name'}), label='')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), label='')
    INSTRUCTOR = "INS"
    STUDENT = "STU"
    roles_choices = [(INSTRUCTOR, "Instructor"), (STUDENT, "Student")]
    role = forms.ChoiceField(choices=roles_choices, label='')

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password1', 'password2']

    def clean(self):
        """
        Verifies that the values entered into the password fields match

        NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
        """
        cleaned_data = super(RegistrationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user_role = UserRole(email_id=self.cleaned_data['email'], role=self.cleaned_data['role'])
        if commit:
            user.save()
            user_role.save()
        return user
