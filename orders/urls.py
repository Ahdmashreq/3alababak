from django.urls import path
from orders import views

app_name = 'orders'
urlpatterns = [
    path('purchase/', views.create_purchase_order_view, name='create-po'),
    path('list/purchase-orders/', views.list_purchase_order_view, name='list-po'),
    path('update/purchase-order/<id>', views.update_purchase_order_view, name='update-po'),
    path('delete/purchase-order/<id>', views.delete_purchase_order_view, name='delete-po'),
    path('sale/', views.create_sales_order_view, name='create-so'),
    path('list/sale-orders/', views.list_sale_order_view, name='list-so'),
    path('update/sale-order/<id>', views.update_sale_order_view, name='update-so'),
    path('delete/sale-order/<id>', views.delete_sale_order_view, name='delete-so'),
    path('purchase/item/<id>', views.get_item, name='get-item'),
    path('po/autocomplete/', views.ItemAutocomplete.as_view(), name='items_list',),

]
