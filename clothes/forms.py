from django.forms import ModelForm
from .models import *
from django import forms
from datetime import date


class DateInput(forms.DateInput):
    input_type = 'date'

class TimePickerInput(forms.TimeInput):
    input_type = 'time'    

today = date.today()

class ClientForm(ModelForm):
    # to include company -User
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ['picked', 'check_out_date', 'check_out_time', 'payment_method','paid']
        widgets = {
            'check_in_date': DateInput(attrs={'min': today}),
            'check_out_date': DateInput(attrs={'min': today}),
            'check_out_time': TimePickerInput(),
            'check_in_time': TimePickerInput(),
        } 

class ClientUpdateForm(ModelForm):
    # to include company -User
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ['check_in_date', 'check_in_time','paid']

        widgets = {
            'check_in_date': DateInput(attrs={'min': today}),
            'check_out_date': DateInput(attrs={'min': today}),
            'check_out_time': TimePickerInput(),
            'check_in_time': TimePickerInput(),

        } 