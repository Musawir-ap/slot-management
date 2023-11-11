from django import forms
from .models import Token, Service


class TokenForm(forms.ModelForm):
    class Meta:
        model = Token
        fields = ['token_time', 'token_date', 'service', 'custom_service', 'description']
        widgets = {
            'token_date': forms.DateInput(attrs={'input_type': 'date', "placeholder": 'date'}),
            'token_time': forms.TimeInput(attrs={'input_type': 'time', "placeholder": 'time'}),
            'service': forms.Select(choices=[(service.code, service.name) for service in Service.objects.all()], ),
            'custom_service': forms.TextInput(attrs={'input_type': 'text', "placeholder": 'other service', "id_":'custom_service_id'}),
            'description': forms.Textarea(attrs={"placeholder": 'description'}),
        }
    
    input_formats = {
            'token_date': ['%Y-%m-%d'], 
            'token_time': ['%I:%M %p'],  
        }
    
