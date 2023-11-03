from django import forms
from django.forms import widgets
from .models import Token, Purpose


class TokenForm(forms.ModelForm):
    class Meta:
        model = Token
        fields = ['token_time', 'token_date', 'purpose', 'description']
        widgets = {
            'token_date': forms.DateInput(attrs={'input_type': 'date', "placeholder": 'date'}),
            'token_time': forms.TimeInput(attrs={'input_type': 'time', "placeholder": 'time'}),
            'purpose': forms.Select(choices=[(purpose.id, purpose.name) for purpose in Purpose.objects.all()], ),
            'description': forms.Textarea(attrs={"placeholder": 'description'}),
        }