from django.shortcuts import render
from .models import *

def index_page(request):
    return render(request, 'content.html')

def tea_blend_creater_form(request):
    return render(request, 'tea_blend_creater.html')

def save_blend(request): 
    return render(request, 'tea_blend_result.html')

def catalog_view(request):
    return render(request, 'catalog.html')

def blend_detail(request):
    return render(request, 'tea_blend_result.html')

def about_view(request):
    return render(request, 'about.html')