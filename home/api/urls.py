from django.urls import path
from home.api import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'api-home'
urlpatterns = [
    path('register/', views.api_register_user, name='register'),
    path('login/', obtain_auth_token, name='login'),

]