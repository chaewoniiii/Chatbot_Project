from itertools import accumulate
from django.http import JsonResponse
from django.shortcuts import render
from matplotlib.font_manager import json_load
from django.views.decorators.csrf import csrf_exempt
import matplotlib.pyplot as plt
from soupsieve import select
from chatbot_admin.model_fit import model_fit
from tensorflow.keras.models import load_model
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
    
    model, x_train, x_test, y_train, y_test = model_fit()
    
    model.fit(x_train, y_train, batch_size=128, shuffle=True, epochs=ep)
    
    context = {
        'loading' : 'fin',
        'learn_data' : ep,
    }
    model.save('./static/data/intent_model_test.h5')
    return JsonResponse(context)

def cb_test(request):
    model, x_train, x_test, y_train, y_test = model_fit()
    model = load_model('./static/data/intent_model_test.h5')
    acc = model.evaluate(x_test, y_test)
    acc = round(acc[1] * 100, 2)
    context = {
        'loading' : 'fin',
        'accu' : acc,
    }
    return JsonResponse(context)