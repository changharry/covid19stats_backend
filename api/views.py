import time

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import csv
import json
from api import csv_data as cd


# Create your views here.

def index(request):
    return HttpResponse('Hello World!')


def global_stats(request):
    json_response = JsonResponse(cd.global_stats(), safe=False)
    json_response["Access-Control-Allow-Origin"] = "*"
    return json_response


def global_total(request):
    json_response = JsonResponse(cd.global_total(), safe=False)
    json_response["Access-Control-Allow-Origin"] = "*"
    return json_response


def regional_stats(request):
    json_response = JsonResponse(cd.region_stats(), safe=False)
    json_response["Access-Control-Allow-Origin"] = "*"
    return json_response


def graph_data(request):
    json_response = JsonResponse(cd.graph_data(), safe=False)
    json_response["Access-Control-Allow-Origin"] = "*"
    return json_response
