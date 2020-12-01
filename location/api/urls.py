from django.urls import path

from location.api import views

app_name = 'api-location'

urlpatterns = [
    path('', views.LocationListView.as_view(), name='list-locations'),
    path('create/', views.api_add_location, name='create-location'),
    path('<slug>/update/', views.api_update_location, name='update-location'),
    path('<slug>/delete/', views.api_delete_location, name='delete-location'),
    path('<slug>/view/', views.api_view_location, name='view-location'),

]
