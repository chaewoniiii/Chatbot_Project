from django.urls import path
from databases import views

urlpatterns = [
    path('', views.test)
]
