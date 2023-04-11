from django.contrib.auth import authenticate

from reuniones import forms
from reuniones.models.Usuario import Usuario


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        max_length=50,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya existe')
        return self.cleaned_data

