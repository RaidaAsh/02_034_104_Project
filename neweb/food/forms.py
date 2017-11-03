from django import forms
from .views import *
from material import *


DISPLAY_CHOICES = (
    ("locationbox", "Display Location"),
    ("displaybox", "Display Direction")
)

class MyForm(forms.Form):
    display_type = forms.ChoiceField(widget=forms.RadioSelect, choices=DISPLAY_CHOICES)
    something_truthy = forms.BooleanField(required=False)


class OrderForm(forms.Form):
    name = forms.CharField()
    company = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    interest = forms.ChoiceField(choices=((None, 'Interested in'), ('D', 'Design'), ('C', 'Development'),
                                          ('I', 'Illustration'), ('B', 'Branding'), ('V', 'Video')))
    budget = forms.ChoiceField(choices=((None, 'Budget'), ('S', 'Less than $5000'), ('M', '$5000-$10000'),
                                        ('L', '$10000-$20000'), ('XL', 'More than $20000')))
    start_date = forms.DateField(label="Expected start date")
    finish_date = forms.DateField(label="Expected finish date")
    attachment = forms.FileField(label="Include some file...")
    message = forms.CharField(widget=forms.Textarea)

    layout = Layout('name', 'company', 'email', 'phone',
                    Row('interest', 'budget'),
                    Row('start_date', 'finish_date'),
                    'attachment', 'message')
