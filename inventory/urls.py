from django.urls import path
from inventory import views

app_name = 'inventory'
urlpatterns = [
               path('category/list/', views.list_categorires_view, name='list-categories'),
               path('category/create/', views.create_category_view, name='create-category'),
               path('category/update/<int:id>', views.update_category_view, name='update-categories'),
               path('category/delete/<int:id>', views.delete_category_view, name='delete-categories'),
               path('brands/list/', views.list_brands_view, name='list-brands'),
               path('brand/create/', views.create_brand_view, name='create-brand'),
               path('brand/update/<int:brand_id>/', views.update_brand_view, name='update-brand'),
               path('brand/delete/<int:brand_id>/', views.delete_brand_view, name='delete-brand'),
               path('attribute/list/', views.list_attributes_view, name='list-attributes'),
               path('attribute/create/', views.create_attribute_view, name='create-attribute'),
               path('attribute/ajax/create/', views.create_attribute_ajax, name='create-attribute-ajax'),
               path('attribute/update/<int:id>', views.update_attribute, name='update-attribute'),
               path('attribute/delete/<int:id>', views.delete_attribute, name='delete-attribute'),
               path('attribute/get-type/<id>', views.get_attribute_type, name='get-attribute-type'),
               path('product/list/', views.list_products_view, name='list-products'),
               path('product/create/', views.create_product_item_view, name='create-product'),
               path('product/view/<int:id>', views.view_item, name='view-item'),
               path('product/update/<int:id>', views.update_item, name='update-item'),
               path('stoke/list/', views.list_stoketake_view, name='list-stokes'),
               path('stoke/create/', views.create_stoketake_view, name='create-stoke'),
               path('uom/create/', views.create_uom_view, name='create-uom'),
               path('uom/update/<int:id>', views.update_uom_view, name='update-uom'),
               path('uom/delete/<int:id>', views.delete_uom_view, name='delete-uom'),
               path('uom/list/', views.list_uom_view, name='list-uom'),
               path('uom-category/create/', views.create_uom_category, name='create-uom-category'),
               path('uom-category/list/', views.list_uom_category, name='list-uom-category'),
               path('uom-category/update/<int:id>', views.update_uom_category, name='update-uom-category'),
               path('uom-category/delete/<int:id>', views.delete_uom_category, name='delete-uom-category'),
               path('stoke_entry/update/<id>', views.update_stoke_entry_view, name='update-stoke-entry'),
               path('stoke_take/update/<id>', views.update_stoke_take_view, name='update-stoke-take'),
               path('stoke_take/list/', views.list_stoketake_entries, name='list-stokes-for-entry'),
               path('stoke_take/delete/<int:id>', views.delete_stoke_take, name='delete-stoke-take'),
               path('stoke_take/view/<int:id>', views.view_stoke, name='print-stoke'),
               path('stoke_take/approval/list', views.list_stoketake_approvals, name='list-stokes-for-approval'),
               path('stoke_take/approve/<id>', views.approve_stoke_view, name='approve-stoke'),


]

