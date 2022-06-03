from itertools import accumulate
from django.http import JsonResponse
from django.shortcuts import render
from matplotlib.font_manager import json_load
from django.views.decorators.csrf import csrf_exempt
import matplotlib.pyplot as plt
from chatbot_admin.model_fit import model_fit
from tensorflow.keras.models import load_model

# Create your views here.
def cb_main(request):
    
    return render(request, 'cb_main.html')

def cb_data(request):
    return render(request, 'cb_data.html')

def cb_req(request):
    return render(request, 'cb_req.html')


@csrf_exempt
def cb_learn(request):
    ep = int(request.POST['ep'])
    
    model, x_train, x_test, y_train, y_test = model_fit()
    if('./static/model.h5'):
        model = load_model('./static/model.h5')

    model.fit(x_train, y_train, batch_size=128, shuffle=True, epochs=ep)
    
    context = {
        'loading' : 'fin',
        'learn_data' : ep,
    }
    model.save('./static/model.h5')
    return JsonResponse(context)

def cb_test(request):
    model, x_train, x_test, y_train, y_test = model_fit()
    model = load_model('./static/model.h5')
    acc = model.evaluate(x_test, y_test)
    acc = round(acc[1] * 100, 2)
    context = {
        'loading' : 'fin',
        'accu' : acc,
    }
    return JsonResponse(context)