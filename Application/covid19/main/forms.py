from django.forms import ModelForm
from .models import *
from django import forms
list = ['ICU Beds', 'Total Population', 'Population Aged 60+', 'Hospital Beds'] #'Income', 'Ventilator Supply',]
list_area = ['County', 'State']
list = [(i,i) for i in list]
list_area = [(i,i) for i in list_area]
class VentilatorForm(ModelForm):
    class Meta:
         model = Ventilator
         fields = ['hospital_name', 'ventilator_number']


class AnalysisType(forms.Form):
    Graph_1_Field_1 = forms.ChoiceField(choices=list)
    Graph_1_Field_2 = forms.ChoiceField(choices=list)
    Graph_2_Field_1 = forms.ChoiceField(choices=list)
    Graph_2_Field_2 = forms.ChoiceField(choices=list)
    area = forms.ChoiceField(choices=list_area)