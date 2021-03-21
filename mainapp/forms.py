import os
from django.forms import (
    ValidationError,
    Form,
    ChoiceField,
    CharField,
    IntegerField,
    TextInput,
    PasswordInput,
    ModelForm,
)
from .models import Machine


class LoginForm(Form):
    login = CharField(
        widget=TextInput(attrs={"placeholder": "Login"}),
    )
    password = CharField(
        widget=PasswordInput(attrs={"placeholder": "Password"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get('login')
        password = cleaned_data.get('password')
        if login == '' and password == '':
            return login, password
        else:
            raise ValidationError('You are not admin')


class MachineForm(ModelForm):
    OS = (
        ('Ubuntu', 'Ubuntu'),
        ('macOS', 'macOS'),
        ('Windows', 'Win'),
    )
    ip_address = CharField(
        label='Machine ip address',
        widget=TextInput(attrs={"placeholder": "ip address"})
    )
    port = IntegerField(label='SSH Port')
    machine_name = CharField(
        label='Machine name',
        widget=TextInput(attrs={"placeholder": "machine name"})
    )
    os = ChoiceField(choices=OS)

    class Meta:
        model = Machine
        fields = ['ip_address', 'port', 'machine_name', 'os']
