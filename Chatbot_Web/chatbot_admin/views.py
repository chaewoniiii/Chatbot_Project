from itertools import accumulate
from django.http import JsonResponse
from django.shortcuts import render
from matplotlib.font_manager import json_load
from django.views.decorators.csrf import csrf_exempt
import matplotlib.pyplot as plt
from soupsieve import select
from .model_fit import *
from .data_check import *
import pandas as pd
import json

# Create your views here.
def cb_main(request):
    result = pd.read_csv('./static/data/total_train_data_1.csv', encoding='cp949')
    bad_count = bad_data_len()
    context = {
        'total_data' : len(result),
        'unknown_data' : bad_count,
    }
    
    return render(request, 'cb_main.html', context)

def cb_data(request):
    if request.method == 'POST':
        s = request.POST.get('r_check')
        res = select_data(s)
        context = {
            'res' : res
        }
        return render(request, 'cb_data.html', context)    
    return render(request, 'cb_data.html')

def cb_req(request):
    return render(request, 'cb_req.html')


@csrf_exempt
def cb_learn(request):
    ep = int(request.POST['ep'])
    intent_fit()
    
    model_fit(ep)
    
    context = {
        'loading' : 'fin',
        'learn_data' : ep,
    }
    
    return JsonResponse(context)

def cb_test(request):
    
    acc = model_eve()
    acc = round(acc[1] * 100, 2)
    context = {
        'loading' : 'fin',
        'accu' : acc,
    }
    return JsonResponse(context)