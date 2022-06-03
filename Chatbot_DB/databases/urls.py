from django.urls import path
from . import views

urlpatterns = [
    path('', views.test),
    path('main/db/', views.db_main),
    path('main/train/', views.db_train),
    path('main/test/', views.db_test),
    path('data/db/', views.db_data),
    path('data/mod/', views.db_mod_data),
    path('chat/db/', views.db_chat),
    path('chat/mod/', views.db_mod_chat)
]
