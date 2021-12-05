from django import  forms
from django.forms import TextInput
from .models import City


# форма заповнення міста
class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('city_name',)
        widgets = {
            'name': TextInput(attrs={'class': 'input', 'placeholder': 'City Name'}),
        }


