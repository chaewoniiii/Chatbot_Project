from django.urls import path
from . import views

app_name = 'cb_admin'
urlpatterns = [
    path("", views.cb_main, name='main'),
    path('cb_data/', views.cb_data, name='data'),
    path('cb_req/', views.cb_req, name='req'),
    path('cb_test/', views.cb_test, name='test'),
    path('cb_learn/', views.cb_learn, name='learn'),
]
