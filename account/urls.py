from django.urls import path
from account import views

app_name = 'account'
urlpatterns = [
    path('customer/', views.create_customer_address_account, name='create-customer'),
    path('supplier/', views.create_supplier_address_account, name='create-supplier'),
    path('list/suppliers/', views.list_suppliers_view, name='list-suppliers'),
    path('list/customers/', views.list_customer_view, name='list-customers'),
    path('company/', views.create_company, name='create-company'),
    path('update/customer/<slug>', views.update_customer_view, name='update-customer'),
    path('update/supplier/<slug>', views.update_supplier_view, name='update-supplier'),
    path('delete/customer/<id>', views.delete_customer, name='delete-customer'),
    path('delete/supplier/<id>', views.delete_supplier, name='delete-supplier'),

]
