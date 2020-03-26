from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.main_page, name='main page'),
    path('query/', views.generic_view, name='generic'),
]