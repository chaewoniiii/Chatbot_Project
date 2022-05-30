from django.shortcuts import render

# Create your views here.
def cb_admin(request):
    return render(request, 'cb_main.html')

def cb_data(request):
    return render(request, 'cb_data.html')

def cb_req(request):
    return render(request, 'cb_req.html')