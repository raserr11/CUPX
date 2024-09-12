from django.shortcuts import render
from django.http import HttpResponse

def upload_file(request):
    return HttpResponse('File Upload')