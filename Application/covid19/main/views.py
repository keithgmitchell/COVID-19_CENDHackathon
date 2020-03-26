from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from .models import *
from django.views.generic import DetailView
# from .filters import *
# import pandas as pd
import plotly.express as px
import plotly.offline as opy
import plotly.graph_objs as go
import plotly.figure_factory as ff
import folium

from .forms import *
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

import folium
import branca
import pandas as pd
import json
import requests


import branca
import pandas as pd
import os
import json
import requests
import folium
import codecs

# Create your views here.
def main_page(request):
    html = 'home.html'
    context = {}
    template = loader.get_template(html)
    return HttpResponse(template.render(context, request))


#####################################
# GRAPHS
#####################################

def GetGraph():
    """
        Making the Pie Chart Summary for the General Views (either for an invoice or a dairy)
    """
    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")
    #figure = ff.create_distplot(values, group_labels, bin_size=200)
    #figure.update_layout(title_text='Distribution of ASV Counts for Heavy Chain vs Light Chain')
    div = opy.plot(fig, auto_open=False, output_type='div')
    return div

def FinalGraphState(arg1, arg2, arg3):
    arg1 = 'State'
    # load geo_json
    with open('../../coronavirus/us-states.geojson') as f:
        geojson_counties = json.load(f)

    # access features
    for i in geojson_counties['features']:
        i['id'] = i['properties']['name']

    # load data associated with geo_json
    pop_df = pd.read_csv('../../JoinedTables/BedsToCovidByState.csv')

    # map
    map_choropleth = folium.Map(location=[39.77, -86.15], zoom_start=3)

    # choropleth
    folium.Choropleth(
        nan_fill_color='white',
        geo_data=geojson_counties,
        name=arg2,
        data=pop_df,
        columns=[arg1, arg2],
        # see folium.Choropleth? for details on key_on
        key_on='feature.id',
        fill_color='PuRd',
        fill_opacity=0.5,
        line_opacity=0.5,
        legend_name=arg2,
        highlight=True
    ).add_to(map_choropleth)


    folium.Choropleth(
        nan_fill_color='white',
        geo_data=geojson_counties,
        name=arg3,
        data=pop_df,
        columns=[arg1, arg3],
        # see folium.Choropleth? for details on key_on
        key_on='feature.id',
        fill_color='GnBu',
        fill_opacity=0.5,
        line_opacity=0.5,
        legend_name=arg3,
        highlight=True
    ).add_to(map_choropleth)


    # layer control to turn choropleth on or off
    folium.LayerControl().add_to(map_choropleth)

    # display map
    return map_choropleth._repr_html_()



def FinalGraphCounty(arg1, arg2, arg3):
    if arg1=='County':
        with codecs.open('../../coronavirus/gz_2010_us_050_00_20m.json', 'r', encoding='utf-8', errors='ignore') as data_file:
            data = json.load(data_file)
        for i in data['features']:
            i['id'] = i['properties']['NAME']


    hospital_beds = pd.read_csv('../../JoinedTables/BedsToCovidByCounty.csv',
                                usecols = ['State', 'County', 'ICU Beds', 'Total Population',
                                           'Population Aged 60+', 'Hospital Beds', 'Confirmed Cases',
                                           'Deaths',  'Normalized Beds', 'Normalized ICU Beds',
                                           'Normalized Cases', 'Normalized Deaths', 'Normalized Deaths 60+'])
    hospital_beds['Deaths'].fillna(0, inplace=True)
    # hospital_beds['ICU Beds'].fillna(NULL, inplace=True)
    hospital_beds['Confirmed Cases'].fillna(0, inplace=True)

    m = folium.Map(location=[48, -102], zoom_start=3)

    folium.Choropleth(
        nan_fill_color='white',
        geo_data=data,
        name=arg2,
        data=hospital_beds,
        columns=[arg1, arg2],
        key_on='feature.id',
        fill_color='PuRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=arg2
    ).add_to(m)

    folium.Choropleth(
        nan_fill_color='white',
        geo_data=data,
        name=arg3,
        data=hospital_beds,
        columns=[arg1, arg3],
        key_on='feature.id',
        fill_color='GnBu',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=arg3
    ).add_to(m)

    folium.LayerControl().add_to(m)

    return m._repr_html_()

#####################################
# VIEWS
#####################################


def generic_view(request):
    context = {}
    context['graph'] = FoliumGraphBeds()
    context['graph2'] = FoliumGraphICUBeds()
    # print(context)
    return render(request, 'generic.html', context)

class VentilatorView(FormView):
    template_name = 'ventilator.html'
    form_class = VentilatorForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def graph_view(request):
    context = {}

    #context['graph1'] = FinalGraph('County', self.field1, self.field2)  # FinalGraph(self.field1, self.field2)
    #context['graph2'] = FinalGraph('County', 'Population Aged 60+',
    #                               'Hospital Beds')  # FinalGraph(self.field1, self.field2)
    context['graph1'] = FinalGraphState('State', 'ICU Beds', 'Confirmed Cases')  # FinalGraph(self.field1, self.field2)

    context['form'] = AnalysisType(initial={'Graph_1_Field_1': 'ICU Beds', 'Graph_1_Field_2':'Confirmed Cases', 'area':'State'})
    if request.method == 'POST':
        form = AnalysisType(request.POST)
        if form.is_valid():
            request.session['form_data'] = form.cleaned_data
            if form.cleaned_data['area'] == 'County':
                context['graph1'] = FinalGraphCounty(form.cleaned_data['area'], form.cleaned_data['Graph_1_Field_1'], form.cleaned_data['Graph_1_Field_2'])  # FinalGraph(self.field1, self.field2)
                #context['graph2'] = FinalGraphCounty(form.cleaned_data['area'], form.cleaned_data['Graph_2_Field_1'], form.cleaned_data['Graph_2_Field_2'])
                context['form'] = AnalysisType(initial={'Graph_1_Field_1': form.cleaned_data['Graph_1_Field_1'], 'Graph_1_Field_2': form.cleaned_data['Graph_1_Field_2'],
                                                    #'Graph_2_Field_1': form.cleaned_data['Graph_2_Field_1'], 'Graph_2_Field_2': form.cleaned_data['Graph_2_Field_2'],
                                                    'area': form.cleaned_data['area']})
            elif form.cleaned_data['area'] == 'State':
                context['graph1'] = FinalGraphState(form.cleaned_data['area'], form.cleaned_data['Graph_1_Field_1'], form.cleaned_data['Graph_1_Field_2'])  # FinalGraph(self.field1, self.field2)
                #context['graph2'] = FinalGraphState(form.cleaned_data['area'], form.cleaned_data['Graph_2_Field_1'], form.cleaned_data['Graph_2_Field_2'])
                context['form'] = AnalysisType(initial={'Graph_1_Field_1': form.cleaned_data['Graph_1_Field_1'], 'Graph_1_Field_2': form.cleaned_data['Graph_1_Field_2'],
                                                    #'Graph_2_Field_1': form.cleaned_data['Graph_2_Field_1'], 'Graph_2_Field_2': form.cleaned_data['Graph_2_Field_2'],
                                                    'area': form.cleaned_data['area']})
    return render(request, 'generic.html', context)

class VentilatorList(ListView):

    model = Ventilator
    template_name = 'ventilator_list.html'
    # paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context