from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),        # / → home page
    path('home/', views.home, name='home'),   # /home → home page
    path('update_value/', views.update_value, name='update_value'),
    path('choose_setting/', views.choose_setting, name='choose_setting'),
    path('home_men/', views.home_men, name='home_men'),
    path('home_women/', views.home_women, name='home_women'),
    path('contact/', views.contact, name='contact'),
    path('contact_successful/', views.contact_successful, name='contact_successful'),
]
