from django.urls import path

from inventory.api import views

app_name = 'api-inventory'

urlpatterns = [
    path('uom-categories/', views.UomCategoriesListView.as_view(), name='list-uom-categories'),
    path('uoms/', views.UomListView.as_view(), name='list-uoms'),
    path('uom-categories/create/', views.api_add_uom_category, name='create-uom-category'),
    path('uoms/create/', views.api_add_uom, name='create-uom'),
    path('uom-categories/<slug>/update/', views.api_update_uom_category, name='update-uom-category'),
    path('uoms/<slug>/update/', views.api_update_uom, name='update-uom'),
    path('uom-categories/<slug>/delete/', views.api_delete_uom_category, name='delete-uom-category'),
    path('uoms/<slug>/delete/', views.api_delete_uom, name='delete-uom'),
    path('uom-categories/<slug>/view/', views.api_view_uom_category, name='view-uom-category'),
    path('uoms/<slug>/view/', views.api_view_uom, name='view-uom'),
    path('categories/', views.CategoriesListView.as_view(), name='list-categories'),
    path('categories/create/', views.api_add_category, name='create-category'),
    path('categories/<slug>/update/', views.api_update_category, name='update-category'),
    path('categories/<slug>/delete/', views.api_delete_category, name='delete-category'),
    path('categories/<slug>/', views.api_view_category, name='view-category'),
    path('brands/', views.BrandsListView.as_view(), name='list-brands'),
    path('brands/create/', views.api_add_brand, name='create-brands'),
    path('brands/<slug>/update/', views.api_update_brand, name='update-brand'),
    path('brands/<slug>/delete/', views.api_delete_brand, name='delete-brand'),
    path('brands/<slug>/', views.api_view_brand, name='view-brand'),
    path('attributes/', views.AttributesListView.as_view(), name='list-attributes'),
    path('attributes/create/', views.api_add_attribute, name='add-attribute'),
    path('attributes/<slug>/update/', views.api_update_attribute, name='update-attribute'),
    path('attributes/<slug>/delete/', views.api_delete_attribute, name='delete-attribute'),
    path('attributes/<slug>/', views.api_view_attribute, name='view-attribute'),

]
