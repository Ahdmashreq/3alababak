from django.urls import path

from account.api import views


app_name = 'api-account'
urlpatterns = [
    path('customers/', views.CustomerListView.as_view(), name='list-customers'),
    path('suppliers/', views.SupplierListView.as_view(), name='list-suppliers'),
    path('customers/create/', views.api_add_customer, name='create-customer'),
    path('customers/<slug>/update/', views.api_update_customer, name='update-customer'),
    path('customers/<slug>/delete/', views.api_delete_customer, name='delete-customer'),
    path('customers/<slug>/view/', views.api_view_customer, name='view-customer'),
    path('suppliers/create/', views.api_add_supplier, name='create-supplier'),
    path('suppliers/<slug>/update/', views.api_update_supplier, name='update-supplier'),
    path('suppliers/<slug>/delete/', views.api_delete_supplier, name='delete-supplier'),
    path('suppliers/<slug>/view/', views.api_view_supplier, name='view-supplier'),


]