from django.http import request
from django.shortcuts import render

def dashboard(request):
    return render(request, 'gestao/dashboard.html')