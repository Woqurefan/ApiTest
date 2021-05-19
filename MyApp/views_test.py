from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from MyApp.models import *
import json
import requests

def test_login_A(request):
    res = {"userid":"uA"}

    return HttpResponse(json.dumps(res),content_type='application/json')


def test_login_B(request):
    res = {"userid":"uB"}

    return HttpResponse(json.dumps(res), content_type='application/json')


def test_api_A(request):
    res = {"errcode":"0"}

    return HttpResponse(json.dumps(res), content_type='application/json')


def test_api_B(request):
    res = {"errcode":"0"}

    return HttpResponse(json.dumps(res), content_type='application/json')
