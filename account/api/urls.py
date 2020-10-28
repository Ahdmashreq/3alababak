from django.urls import path

from account.api import views


app_name = 'api-account'
urlpatterns = [
    path('customers/', views.api_list_customers, name='list-customers'),
    path('suppliers/', views.api_list_suppliers, name='list-suppliers'),
]