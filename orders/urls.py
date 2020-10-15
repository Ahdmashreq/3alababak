from django.conf.urls import url
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
    path('po/autocomplete/', views.ItemAutocomplete.as_view(), name='items_list', ),
    path('list/receivings/<int:id>', views.list_receiving, name='list-receiving', ),
    path('create/receiving-transactions/<int:id>', views.create_receiving, name='create-receiving', ),
    path('list/purchases-for-receiving/', views.list_purchases_for_receiving, name='list-po-for-receiving'),
    path('so_transaction/autocomplete/', views.SoItemAutocomplete.as_view(), name='sell-items', ),
    path('create/receiving-transactions2/<int:id>', views.create_receiving2, name='create-receiving2', ),
    path('po/receipt/<id>', views.view_received, name='view-rec'),
    path('po/view/<id>/<flag>', views.view_purchase_order, name='view-po'),
    path('po/view/<id>', views.view_sale_order, name='view-so'),

]
