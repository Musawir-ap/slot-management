from django import forms
from django.forms import widgets
from .models import Token, Service


class TokenForm(forms.ModelForm):
    class Meta:
        model = Token
        fields = ['token_time', 'token_date', 'service', 'description']
        widgets = {
            'token_date': forms.DateInput(attrs={'input_type': 'date', "placeholder": 'date'}),
            'token_time': forms.TimeInput(attrs={'input_type': 'time', "placeholder": 'time'}),
            'service': forms.Select(choices=[(service.id, service.name) for service in Service.objects.all()], ),
            'description': forms.Textarea(attrs={"placeholder": 'description'}),
        }