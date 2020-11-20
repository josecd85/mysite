from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.redirect_login, name='redirect_login'),
    path('home', views.home, name='home'),
    path('alert/<int:pk>/', views.alert_detail, name='alert_detail'),
    path('examples', views.examples, name='examples'),
    path('reset_pass', views.reset_pass, name='reset_pass'),
    path('alerts', views.alerts, name='alerts'),
    path('load_file', views.load_file, name='load_file'),
]
