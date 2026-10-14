from django.urls import path
from gestao import views

urlpatterns = [
    path('', views.dashboard, name='dashboard')
]