from django.urls import path
from location import views

app_name = 'location'

urlpatterns = [
    path('create/<l_type>', views.create_location_view, name='create-location'),
    path('update/<slug>', views.update_location_view, name='update-location'),
    path('list/locations/<l_type>', views.list_location_view, name='list-locations'),
    path('delete/<slug>', views.delete_location_view, name='delete-location'),
]
