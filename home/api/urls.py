from django.urls import path

from home.api import views


app_name = 'api-home'
urlpatterns = [
    path('register/', views.api_register_user, name='register'),
]