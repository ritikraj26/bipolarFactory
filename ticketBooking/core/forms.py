from django import forms
from .models import Flight
from django.contrib.auth.models import User

class FlightSearchForm(forms.Form):
    origin = forms.CharField(label="Origin City", max_length=100)
    destination = forms.CharField(label="Destination City", max_length=100)
    departure_date = forms.DateField(label="Departure Date", widget=forms.DateInput(attrs={'type': 'date'}))

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        
class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    