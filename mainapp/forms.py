import os
from django.forms import (
    ValidationError,
    Form,
    CharField,
    TextInput,
    PasswordInput,
)


class LoginForm(Form):
    login = CharField(
        label='',
        max_length=100,
        widget=TextInput(attrs={"placeholder": "Login"}),
    )
    password = CharField(
        label='',
        max_length=100,
        widget=PasswordInput(attrs={"placeholder": "Password"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get('login')
        password = cleaned_data.get('password')
        if login == os.getenv('ADMIN_LOGIN') and password == os.getenv('ADMIN_PASSWORD'):
            return login, password
        else:
            raise ValidationError('You are not admin')
