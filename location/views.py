from django.shortcuts import render, redirect
from django.contrib import messages
from location.models import Location
from location.forms import LocationCreationForm
from orders.utils import get_seq


def list_location_view(request, l_type):
    mytype = ''
    if l_type == 'w':
        mytype = 'warehouse'
    elif l_type == 's':
        mytype = 'store'
    locations_list = Location.objects.filter(type=mytype)
    location_context = {
        'locations_list': locations_list,
        'type': l_type,
        'title': 'Warehouses' if l_type == 'w' else 'Stores'
    }
    return render(request, 'list-locations.html', location_context)


def create_location_view(request, l_type):
    location_form = LocationCreationForm()
    if l_type == 'w':
        title = 'New Warehouse'
    elif l_type == 's':
        title = 'New Store'

    if request.method == 'POST':
        location_form = LocationCreationForm(request.POST)
        if location_form.is_valid():
            location_obj = location_form.save(commit=False)
            if l_type == 'w':
                rows_number = Location.objects.filter(type='warehouse').count()
                location_obj.type = 'warehouse'
                location_obj.code = "W-" + get_seq(rows_number)
            elif l_type == 's':
                rows_number = Location.objects.filter(type='store').count()
                location_obj.type = 'store'
                location_obj.code = "S-" + get_seq(rows_number)

            location_obj.created_by = request.user
            location_obj.company = request.user.company
            location_obj.save()
            messages.success(request, 'Saved Successfully')
            if 'Save and exit' in request.POST:
                return redirect('location:list-locations', l_type=l_type)
            elif 'Save and add' in request.POST:
                return redirect('location:create-location', l_type=l_type)
    location_context = {
        'location_form': location_form,
        'title': title,
        'type': l_type,
    }
    return render(request, 'create-location.html', location_context)


def update_location_view(request, slug):
    location = Location.objects.get(slug=slug)
    title = 'Update Warehouse' if location.type == 'warehouse' else 'Update Store'
    mytype = 'w' if location.type == 'warehouse' else 's'
    if request.method == 'POST':
        location_form = LocationCreationForm(request.POST, instance=location)
        if location_form.is_valid():
            location_obj = location_form.save(commit=False)
            location_obj.created_by = request.user
            location_obj.company = request.user.company
            location_obj.save()
            if 'Save and exit' in request.POST:
                return redirect('location:list-locations', l_type=mytype)
    else:
        location_form = LocationCreationForm(instance=location)
    location_context = {
        'location_form': location_form,
        'title': title,
        'type': mytype,
        'update': True,

    }
    return render(request, 'create-location.html', location_context)


def delete_location_view(request, slug):
    location = Location.objects.get(slug=slug)
    mytype = 'w' if location.type == 'warehouse' else 's'

    try:
        location.delete()
    except BaseException as e:
        print(e)
    return redirect('location:list-locations',l_type=mytype)
