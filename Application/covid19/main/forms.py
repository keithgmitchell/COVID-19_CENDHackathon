from django.forms import ModelForm
from .models import *
from django import forms
cases_list = ['Total Population', 'Population Aged 60+', 'Confirmed Cases', 'Deaths', 'Normalized Cases', 'Normalized Deaths', 'Normalized Deaths 60+', ]
#'Income', 'Ventilator Supply',]
resource_list = ['ICU Beds', 'Hospital Beds', 'Normalized Beds', 'Normalized ICU Beds']
list_area = ['County', 'State']
cases_list = [(i,i) for i in cases_list]
resource_list = [(i,i) for i in resource_list]
list_area = [(i,i) for i in list_area]
class VentilatorForm(ModelForm):
    class Meta:
         model = Ventilator
         fields = ['hospital_name', 'ventilator_number']


class AnalysisType(forms.Form):
    Graph_1_Field_1 = forms.ChoiceField(choices=cases_list)
    Graph_1_Field_2 = forms.ChoiceField(choices=resource_list)
    #Graph_2_Field_1 = forms.ChoiceField(choices=list)
    #Graph_2_Field_2 = forms.ChoiceField(choices=list)
    area = forms.ChoiceField(choices=list_area)