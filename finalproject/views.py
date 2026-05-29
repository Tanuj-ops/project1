from django.http import HttpResponse
from django.shortcuts import render

def h1(request):
    return HttpResponse("Welcome to the home page!")