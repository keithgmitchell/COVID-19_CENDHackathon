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

# Create your views here.
def main_page(request):
    html = 'home.html'
    context = {}
    template = loader.get_template(html)
    return HttpResponse(template.render(context, request))




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

def generic_view(request):
    context = {}
    context['graph'] = GetGraph()
    # print(context)
    return render(request, 'generic.html', context)



