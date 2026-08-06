from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Email Address"
        })
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "username": "Username",
            "password1": "Password",
            "password2": "Confirm Password",
        }

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

            if field in placeholders:
                self.fields[field].widget.attrs["placeholder"] = placeholders[field]

        # Remove Django's default help text
        self.fields["username"].help_text = None
        self.fields["password1"].help_text = None
        self.fields["password2"].help_text = None
class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
            }
        )
    )