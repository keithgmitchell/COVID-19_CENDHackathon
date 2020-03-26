from django.urls import path, include

from . import views

urlpatterns = [
    path('information/', views.main_page, name='main page'),
    path('query/', views.graph_view, name='generic'),
    path('', views.graph_view, name='generic'),
    path('ventilator/', views.VentilatorView.as_view(), name='generic'),
    path('ventilator_list/', views.VentilatorList.as_view(), name='generic'),
    path('table/', views.test_view, name='generic'),
]