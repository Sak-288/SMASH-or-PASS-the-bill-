from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),        # / → home page
    path('home/', views.home, name='home'),   # /home → home page
]