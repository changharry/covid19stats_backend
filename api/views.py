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


def g_total(request):
    json_response = JsonResponse(cd.g_total(), safe=False)
    json_response["Access-Control-Allow-Origin"] = "*"
    return json_response


def g_total_change(request):
    json_response = JsonResponse(cd.g_total_change(), safe=False)
    json_response["Access-Control-Allow-Origin"] = "*"
    return json_response


def g_total_rate_change(request):
    json_response = JsonResponse(cd.g_total_rate_change(), safe=False)
    json_response["Access-Control-Allow-Origin"] = "*"
    return json_response


def r_total(request, country):
    json_response = JsonResponse(cd.r_total(country), safe=False)
    json_response["Access-Control-Allow-Origin"] = "*"
    return json_response


def r_change(request, country):
    json_response = JsonResponse(cd.r_change(country), safe=False)
    json_response["Access-Control-Allow-Origin"] = "*"
    return json_response


def r_rate_change(request, country):
    json_response = JsonResponse(cd.r_rate_change(country), safe=False)
    json_response["Access-Control-Allow-Origin"] = "*"
    return json_response


def r_delta_rate_change(request, country):
    json_response = JsonResponse(cd.r_delta_rate_change(country), safe=False)
    json_response["Access-Control-Allow-Origin"] = "*"
    return json_response


def g_delta_rate_change(request):
    json_response = JsonResponse(cd.g_delta_rate_change(), safe=False)
    json_response["Access-Control-Allow-Origin"] = "*"
    return json_response
