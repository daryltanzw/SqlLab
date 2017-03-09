from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Email'}), label='')
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}), label='')

    class Meta:
        fields = ['email', 'password']
