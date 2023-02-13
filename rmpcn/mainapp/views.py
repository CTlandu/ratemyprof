from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "index.html")

def instructor_result(request):
    return render(request, "instru_result.html")

def instructor_detail(request):
    return render(request, "instru_detail.html")

def profile_basic(request):
    return render(request, "profile_basic.html")