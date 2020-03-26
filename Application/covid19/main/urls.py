from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.main_page, name='main page'),
    path('query/', views.graph_view, name='generic'),
    path('ventilator/', views.VentilatorView.as_view(), name='generic'),
    path('ventilator_list/', views.VentilatorList.as_view(), name='generic'),
]