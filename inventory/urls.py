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

]
