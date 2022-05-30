from django.urls import path
from . import views

app_name = 'cb_admin'
urlpatterns = [
    path("", views.cb_admin, name='main'),
    path('cb_data', views.cb_data, name='data'),
    path('cb_req', views.cb_req, name='req'),
]
