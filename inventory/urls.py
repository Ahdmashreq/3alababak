from django.urls import path
from inventory import views

app_name = 'inventory'
urlpatterns = [
               path('category/list/', views.list_categorires_view, name='list-categories'),
               path('category/create/', views.create_category_view, name='create-category'),
               path('brands/list/', views.list_brands_view, name='list-brands'),
               path('brand/create/', views.create_brand_view, name='create-brand'),
               path('attribute/list/', views.list_attributes_view, name='list-attributes'),
               path('attribute/create/', views.create_attribute_view, name='create-attribute'),
               path('product/list/', views.list_products_view, name='list-products'),
               path('product/create/', views.create_product_item_view, name='create-product'),
               path('stoke/list/', views.list_stoketake_view, name='list-stokes'),
               path('stoke/create/', views.create_stoketake_view, name='create-stoke'),
               path('uom/create/', views.create_uom_view, name='create-uom'),
               path('uom/list/', views.list_uom_view, name='list-uom'),
               path('stoke_entry/update/<id>', views.update_stoke_entry_view, name='update-stoke-entry'),
               path('stoke_take/update/<id>', views.update_stoke_take_view, name='update-stoke-take'),
               path('stoke_take/list/', views.list_stoketake_entries, name='list-stokes-for-entry'),
               path('stoke_take/delete/<int:id>', views.delete_stoke_take, name='delete-stoke-take'),
               path('stoke_take/view/<int:id>', views.view_stoke, name='print-stoke'),
               path('stoke_take/approval/list', views.list_stoketake_approvals, name='list-stokes-for-approval'),
               path('stoke_take/approve/<id>', views.approve_stoke_view, name='approve-stoke'),
]
