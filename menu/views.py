from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Projeto em construção. Acesse /admin/")
