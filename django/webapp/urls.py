from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),        # for root URL (e.g. /)
    path('home/', views.home, name='home'),   # for /home URL
]