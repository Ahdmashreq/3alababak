import json
from datetime import date

from django.http import JsonResponse

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Q, ProtectedError
from django.shortcuts import render, redirect
from django.contrib import messages
from inventory.models import (Category, Brand, Product, Attribute, Item, Uom, StokeTake, StokeEntry, UomCategory,
                              ItemAttributeValue, ItemImage)
from inventory.forms import (CategoryForm, category_model_formset, BrandForm, brand_model_formset,
                             AttributeForm, attribute_model_formset, ProductForm,
                             uom_formset, StokeTakeForm, UOMForm, stoke_entry_formset, StokeEntryForm, UomCategoryForm,
                             ItemForm, item_attribute_model_formset, ItemImageForm)
from inventory.serializers import AttributeSeializer
from orders.models import Inventory_Balance, MaterialTransaction1, MaterialTransactionLines
import random
from orders.utils import get_seq, ItemSerializer, JSONResponse
from django.http import HttpResponse
from django.db import IntegrityError


def create_category_view(request):
    category_form = CategoryForm(user=request.user)
    if request.method == 'POST':
        category_form = CategoryForm(request.POST, user=request.user)
        if category_form.is_valid():
            category_obj = category_form.save(commit=False)
            category_obj.company = request.user.company
            category_obj.created_by = request.user
            try:
                category_obj.save()
                if 'Save and exit' in request.POST:
                    return redirect('inventory:list-categories')
                elif 'Save and add' in request.POST:
                    return redirect('inventory:create-category')
            except IntegrityError:
                messages.error(request, "Category name already exists")

    categoryContext = {
        'category_form': category_form,
        'title': 'New Category'

    }
    return render(request, 'create-category.html', context=categoryContext)


def list_categorires_view(request):
    categories_list = Category.objects.filter(company=request.user.company)
    categoryContext = {
        'categories_list': categories_list
    }
    return render(request, 'list-categories.html', context=categoryContext)


def list_brands_view(request):
    brands_list = Brand.objects.filter(company=request.user.company)
    brandsContext = {
        'brands_list': brands_list
    }
    return render(request, 'list-brands.html', context=brandsContext)


def create_brand_view(request):
    brand_form = BrandForm()
    if request.method == 'POST':
        brand_form = BrandForm(request.POST)
        if brand_form.is_valid():
            brand_obj = brand_form.save(commit=False)
            brand_obj.company = request.user.company
            brand_obj.created_by = request.user
            try:
                brand_obj.save()
                if 'Save and exit' in request.POST:
                    return redirect('inventory:list-brands')
                elif 'Save and add' in request.POST:
                    return redirect('inventory:create-brand')

            except IntegrityError:
                messages.error(request, "Brand name already exists")

    categoryContext = {
        'brand_form': brand_form,
        'title': 'New Brand'

    }
    return render(request, 'create-brand.html', context=categoryContext)


def update_brand_view(request, brand_id):
    required_brand = Brand.objects.get(id=brand_id)
    brand_form = BrandForm(instance=required_brand)
    if request.method == 'POST':
        brand_form = BrandForm(request.POST, instance=required_brand)
        if brand_form.is_valid():
            brand_obj = brand_form.save(commit=False)
            brand_obj.last_updated_by = request.user
            try:
                brand_obj.save()
                if 'Save and exit' in request.POST:
                    return redirect('inventory:list-brands')
            except IntegrityError:
                messages.error(request, "Brand name already exists")

    categoryContext = {
        'brand_form': brand_form,
        'title': 'Update {}'.format(required_brand),
        'update_flag': True,
    }
    return render(request, 'create-brand.html', context=categoryContext)


def delete_brand_view(request, brand_id):
    required_brand = Brand.objects.get(id=brand_id)
    try:
        required_brand.delete()
    except ProtectedError:
        error_message = "This object can't be deleted!!"
        messages.error(request, error_message)
    return redirect('inventory:list-brands')


def list_attributes_view(request):
    attributes_list = Attribute.objects.filter(company=request.user.company)
    attributesContext = {
        'attributes_list': attributes_list
    }
    return render(request, 'list-attributes.html', context=attributesContext)


def create_attribute_view(request):
    attribute_form = AttributeForm()
    if request.method == 'POST':
        attribute_form = AttributeForm(request.POST)
        if attribute_form.is_valid():
            attribute_obj = attribute_form.save(commit=False)
            attribute_obj.company = request.user.company
            attribute_obj.created_by = request.user
            try:
                attribute_obj.save()
                if 'Save and exit' in request.POST:
                    return redirect('inventory:list-attributes')
                elif 'Save and add' in request.POST:
                    return redirect('inventory:create-attribute')
            except IntegrityError:
                messages.error(request, "Attribute name and type already exit")

    attributeContext = {
        'attribute_form': attribute_form,
        'title': 'New Attribute'

    }
    return render(request, 'create-attribute.html', context=attributeContext)


def list_products_view(request):
    products_list = Item.objects.filter(company=request.user.company)
    productsContext = {
        'products_list': products_list
    }
    return render(request, 'list-products.html', context=productsContext)


def create_product_item_view(request):
    product_form = ProductForm(user=request.user)
    uom_category_form = UomCategoryForm()
    item_form = ItemForm(user=request.user)
    item_attribute_form = item_attribute_model_formset()
    attribute_form = AttributeForm()
    image_form = ItemImageForm()
    if request.is_ajax():
        uom = Uom.objects.filter(company=request.user.comapny)
        return JsonResponse(list(uom.values()), safe=False)

    if request.method == 'POST':

        product_form = ProductForm(request.POST, user=request.user)
        item_form = ItemForm(request.POST, user=request.user)
        item_attribute_form = item_attribute_model_formset(request.POST)
        image_form = ItemImageForm(request.POST, request.FILES)

        if product_form.is_valid() and item_form.is_valid() and item_attribute_form.is_valid() and image_form.is_valid():
            product_obj = product_form.save(commit=False)
            product_obj.company = request.user.company
            product_obj.created_by = request.user
            product_obj.save()
            item_obj = item_form.save(commit=False)
            item_obj.company = request.user.company
            item_obj.product = product_obj
            item_obj.created_by = request.user
            try:
                item_obj.save()
            except IntegrityError as e:
                messages.error(request , 'SKU must be unique')
                attributeContext = {
                    'title': "New Item",
                        'product_form': product_form,
                        'item_form': item_form,
                        'item_attribute_formset': item_attribute_form,
                        'attribute_form': attribute_form,
                        'image_form': image_form,

                }
                return render(request, 'create-product-item.html', context=attributeContext)
            image_obj = image_form.save(commit=False)
            image_obj.created_by = request.user
            image_obj.item = item_obj
            image_obj.save()
            item_attribute_form = item_attribute_model_formset(request.POST, instance=item_obj)
            if item_attribute_form.is_valid():
                for form in item_attribute_form:
                    temp_value = form.cleaned_data['temp_value']
                    att_obj = form.save(commit=False)
                    att_obj.value = temp_value
                    att_obj.created_by = request.user
                    att_obj.save()
                if 'Save and exit' in request.POST:
                    return redirect('inventory:list-products')
                elif 'Save and add' in request.POST:
                    return redirect('inventory:create-product')
                else:
                    return redirect('inventory:view-item', id=item_obj.id)
        elif item_form.is_valid() == False:
            messages.error(request , item_form.errors)

    attributeContext = {
        'title': "New Item",
        'product_form': product_form,
        'item_form': item_form,
        'item_attribute_formset': item_attribute_form,
        'attribute_form': attribute_form,
        'image_form': image_form,
        'uom_category_form': uom_category_form,

        }
    return render(request, 'create-product-item.html', context=attributeContext)


def list_stoketake_view(request):
    stoke_list = StokeTake.objects.filter(company=request.user.company)
    stokes_context = {
        "title": "Stoke Takings",
        'stoke_list': stoke_list
    }
    return render(request, 'list-stokes.html', context=stokes_context)


def create_uom_view(request, category_id):
    uom_form = UOMForm()
    uom_category = UomCategory.objects.get(id=category_id)
    if request.method == 'POST':
        uom_form = UOMForm(request.POST)
        uom_form.instance.category = uom_category
        uom_form.instance.company = request.user.company
        if uom_form.is_valid():
            uom_obj = uom_form.save(commit=False)
            uom_obj.created_by = request.user
            try:
                uom_obj.save()
                if 'Save and exit' in request.POST:
                    return redirect('inventory:list-uom', category_id=category_id)
                elif 'Save and add' in request.POST:
                    return redirect('inventory:create-uom', category_id=category_id)
            except IntegrityError:
                messages.error(request, "UOM name already exists")
        else:
            messages.error(request, "UOM is not valid :{}".format(uom_form.errors))
            print(uom_form.errors)
    uom_context = {
        'uom_from': uom_form,
        'title': 'New UOM for {}'.format(uom_category),
        'category_id': category_id,
    }
    return render(request, 'create-uom.html', context=uom_context)


def list_uom_view(request, category_id):
    uom_list = Uom.objects.filter(company=request.user.company, category=category_id)
    category = UomCategory.objects.get(id=category_id)
    uom_context = {
        'uom_list': uom_list,
        'category_id': category_id,
        'title': "Uoms for {} category".format(category),
    }
    return render(request, 'list-uom.html', context=uom_context)


def update_uom_view(request, id):
    uom = Uom.objects.get(id=id)
    category = uom.category
    uom_form = UOMForm(instance=uom)
    if request.method == 'POST':
        uom_form = UOMForm(request.POST, instance=uom)
        if uom_form.is_valid():
            uom_obj = uom_form.save(commit=False)
            uom_obj.last_updated_by = request.user
            try:
                uom_obj.save()
                if 'Save and exit' in request.POST:
                    return redirect('inventory:list-uom', category_id=category.id)
            except IntegrityError:
                messages.error(request, "UOM name already exists")
        else:
            messages.error(request, "UOM is not valid :{}".format(uom_form.errors))
            print(uom_form.errors)
    uom_context = {
        'uom_from': uom_form,
        'title': 'Update UOM',
        'update': True,
        'category_id': category.id,

    }
    return render(request, 'create-uom.html', context=uom_context)


def delete_uom_view(request, id):
    required_uom = Uom.objects.get(id=id)
    category = required_uom.category
    try:
        required_uom.delete()
    except ProtectedError:
        error_message = "This object can't be deleted!!"
        messages.error(request, error_message)
    return redirect('inventory:list-uom', category_id=category.id)


def create_stoke_entries_template(type, stoke_take_obj,user):
    items = []
    location = stoke_take_obj.location
    if type == 'location':
        inventory_balance = Inventory_Balance.objects.filter(location=location)
        for record in inventory_balance:
            items.append(record.item)
    elif type == 'category':
        category = stoke_take_obj.category
        descendants = Category.objects.get(id=category.id).get_descendants(include_self=True)
        products = Product.objects.filter(Q(category__parent__in=descendants) | Q(category__in=descendants))
        myitems = Item.objects.filter(product__in=products)
        inventory_balance = Inventory_Balance.objects.filter(location=location, item__in=myitems)
        for record in inventory_balance:
            items.append(record.item)
    elif type == 'random':
        inventory_balance = Inventory_Balance.objects.filter(location=location)
        item_list = []
        for record in inventory_balance:
            item_list.append(record.item)
        number_of_items = stoke_take_obj.random_number
        items = random.sample(item_list, number_of_items)
    entry_list = []
    for item in items:
        entry_list.append(StokeEntry(stoke_take=stoke_take_obj, item=item, created_by=user))
    try:
        StokeEntry.objects.bulk_create(entry_list)
    except BaseException:
        return False
    return True


def create_stoketake_view(request):
    stoke_form = StokeTakeForm(update=False, user=request.user)
    stoke_context = {}
    items = []
    if request.method == 'POST':
        stoke_form = StokeTakeForm(request.POST, update=False, user=request.user)
        if stoke_form.is_valid():
            stoke_obj = stoke_form.save(commit=False)
            stoke_obj.created_by = request.user
            stoke_obj.company = request.user.company
            name = stoke_obj.name
            date = stoke_obj.date
            type = stoke_obj.type
            location = stoke_obj.location
            stoke_context['name'] = name
            stoke_context['date'] = date
            stoke_context['type'] = type
            stoke_context['location'] = location
            # TODO: Need to be refactored to achieve separation of concerns
            if type == 'location':
                inventory_balance = Inventory_Balance.objects.filter(location=location)
                for record in inventory_balance:
                    items.append(record.item)
            elif type == 'category':
                category = stoke_obj.category
                descendants = Category.objects.get(id=category.id).get_descendants(include_self=True)
                products = Product.objects.filter(Q(category__parent__in=descendants) | Q(category__in=descendants))
                myitems = Item.objects.filter(product__in=products)
                inventory_balance = Inventory_Balance.objects.filter(location=location, item__in=myitems)
                for record in inventory_balance:
                    items.append(record.item)
                stoke_context['category'] = category
            elif type == 'random':
                inventory_balance = Inventory_Balance.objects.filter(location=location)
                item_list = []
                for record in inventory_balance:
                    item_list.append(record.item)
                number_of_items = stoke_form.cleaned_data['random_number']
                items = random.sample(item_list, number_of_items)
            stoke_obj.save()
            entry_list = []
            for item in items:
                entry_list.append(StokeEntry(stoke_take=stoke_obj, item=item, created_by=request.user))
            StokeEntry.objects.bulk_create(entry_list)
            stoke_context['items'] = items
            messages.success(request, 'Stoke Take created successfully')
            if 'Save and exit' in request.POST:
                return redirect('inventory:list-stokes')
            elif 'Save and print' in request.POST:
                return render(request, 'stoke-entry-template.html', context=stoke_context)
            # return redirect('inventory:create-stoke')

        else:
            messages.error(request, 'Form is not Valid')

    stoke_context = {
        'stoke_form': stoke_form,
        'title': 'New Stoke Taking'

    }
    return render(request, 'create-stoke.html', context=stoke_context)


def update_stoke_take_view(request, id):
    stoke_inst = StokeTake.objects.get(id=id)
    stoke_form = StokeTakeForm(update=False, instance=stoke_inst, user=request.user)
    items = []

    if request.method == 'POST':
        stoke_form = StokeTakeForm(request.POST, update=False, instance=stoke_inst, user=request.user)
        if stoke_form.is_valid():
            stoke_obj = stoke_form.save(commit=False)
            stoke_obj.last_updated_by = request.user
            location = stoke_obj.location
            if stoke_obj.type == 'location':
                stoke_obj.category = None
                inventory_balance = Inventory_Balance.objects.filter(location=location)
                for record in inventory_balance:
                    items.append(record.item)
            elif stoke_obj.type == 'category':
                category = stoke_obj.category
                descendants = Category.objects.get(name=category).get_descendants(include_self=True)
                products = Product.objects.filter(Q(category__parent__in=descendants) | Q(category__in=descendants))
                myitems = Item.objects.filter(product__in=products)
                inventory_balance = Inventory_Balance.objects.filter(location=location, item__in=myitems)
                for record in inventory_balance:
                    items.append(record.item)
            elif stoke_obj.type == 'random':
                stoke_obj.category = None
                inventory_balance = Inventory_Balance.objects.filter(location=location)
                item_list = []
                for record in inventory_balance:
                    item_list.append(record.item)
                number_of_items = stoke_form.cleaned_data['random_number']
                items = random.sample(item_list, number_of_items)
            stoke_obj.save()
            stoke_entry_instances = StokeEntry.objects.filter(stoke_take=stoke_obj)
            stoke_entry_instances.delete()
            entry_list = []
            for item in items:
                entry_list.append(StokeEntry(stoke_take=stoke_obj, item=item, created_by=request.user))
            StokeEntry.objects.bulk_create(entry_list)
            messages.success(request, 'Updated Successfully')
            if 'Save and exit' in request.POST:
                return redirect('inventory:list-stokes')
            elif 'Save and print' in request.POST:
                return redirect('inventory:print-stoke', id=id)
        else:
            messages.error(request, 'Form is not valid')

    context = {'stoke_form': stoke_form, 'title': 'Update Stoke Taking'}
    return render(request, 'create-stoke.html', context=context)


def list_stoketake_entries(request):
    stoke_list = StokeTake.objects.filter(company=request.user.company).exclude(status='Approved')
    context = {"title": "Stoke Taking Entries", "entry_mode": True, 'stoke_list': stoke_list}

    return render(request, 'list-stokes.html', context=context)


def update_stoke_entry_view(request, id):
    stoke_obj = StokeTake.objects.get(id=id)
    stoke_take_form = StokeTakeForm(update=True, instance=stoke_obj, user=request.user)
    stoke_entry_inline_formset = stoke_entry_formset(instance=stoke_obj, form_kwargs={'approve': False})

    if request.method == 'POST':
        stoke_entry_inline_formset = stoke_entry_formset(request.POST, instance=stoke_obj,
                                                         form_kwargs={'approve': False})
        if stoke_entry_inline_formset.is_valid():
            stoke_entry_obj = stoke_entry_inline_formset.save(commit=False)
            for stoke_entry in stoke_entry_obj:
                stoke_entry.last_updated_by = request.user
                stoke_entry.save()

            if 'send' in request.POST:
                if len(StokeEntry.objects.filter(stoke_take=stoke_obj, quantity=None)) != 0:
                    messages.error(request, 'You must fill all quantities')
                else:
                    stoke_obj.status = 'Pending Approval'
                    stoke_obj.save()
                    return redirect('inventory:list-stokes-for-entry')

            if len(StokeEntry.objects.filter(stoke_take=stoke_obj).exclude(quantity=None)) > 0:
                stoke_obj.status = 'In Progress'
                stoke_obj.save()

            if 'Save and exit' in request.POST:
                return redirect('inventory:list-stokes-for-entry')

    sub_context = {'title': "Create Entries", 'stoke_entry_inlineformset': stoke_entry_inline_formset,
                   'stoke_form': stoke_take_form}

    return render(request, 'update-stoke.html', context=sub_context)


def delete_stoke_take(request, id):
    stoke_take = StokeTake.objects.get(pk=id)
    print(stoke_take.status)
    if stoke_take.status == 'In Progress' or stoke_take.status == 'Done':
        messages.error(request, "Stoke taking cannot be deleted while in progress")
    else:
        deleted = stoke_take.delete()
        if deleted:
            messages.success(request, "Deleted Successfully")
        else:
            messages.error(request, "Error Not deleted")
    return redirect('inventory:list-stokes')


def view_stoke(request, id):
    stoke_obj = StokeTake.objects.get(id=id)
    stoke_context = {}
    name = stoke_obj.name
    date = stoke_obj.date
    type = stoke_obj.type
    location = stoke_obj.location
    stoke_context['name'] = name
    stoke_context['date'] = date
    stoke_context['type'] = type
    stoke_context['location'] = location
    stoke_entries = StokeEntry.objects.select_related().filter(stoke_take=stoke_obj)
    items = [stoke_entry.item for stoke_entry in stoke_entries]
    if type == 'location':
        location = stoke_obj.location
        #items = Inventory_Balance.objects.filter(location=location)
    elif type == 'category':
        category = stoke_obj.category
        descendants = Category.objects.get(name=category).get_descendants(include_self=True)
        products = Product.objects.filter(Q(category__parent__in=descendants) | Q(category__in=descendants))
        #items = Inventory_Balance.objects.filter(item__product__in=products)
        stoke_context['category'] = category
    elif type == 'all':
        pass
        #items = Inventory_Balance.objects.all()
    elif type == 'random':
        stoke_entries = StokeEntry.objects.select_related().filter(stoke_take=stoke_obj)
        #items = [stoke_entry.item for stoke_entry in stoke_entries]

    stoke_context['items'] = items
    return render(request, 'stoke-entry-template.html', context=stoke_context)


def list_stoketake_approvals(request):
    stoke_list = StokeTake.objects.filter(Q(status='Pending Approval'),
                                          company=request.user.company)
    context = {"entry_mode": True, 'stoke_list': stoke_list}
    return render(request, 'list-stoke-approvals.html', context=context)


def approve_stoke_view(request, id):
    stoke_obj = StokeTake.objects.get(id=id)
    stoke_entries = StokeEntry.objects.filter(stoke_take=stoke_obj)
    entries = []
    for stoke_entry in stoke_entries:
        inventory = Inventory_Balance.objects.filter(item=stoke_entry.item, location=stoke_obj.location)
        on_hand = inventory[0].qnt
        category = stoke_entry.item.product.category
        entries.append({'category': category, 'brand': stoke_entry.item.product.brand,
                        'item': stoke_entry.item, 'uom': stoke_entry.item.uom, 'on_hand': on_hand,
                        'quantity': stoke_entry.quantity})

    status = stoke_obj.status

    if request.method == 'POST':
        if 'approve' in request.POST:
            success = create_stoke_transaction(stoke_obj, request.user)
            if success:
                StokeTake.objects.filter(id=id).update(status='Approved')
                messages.success(request, 'Stoke record is approved, Inventory is updated')
            else:
                messages.error(request, 'Error in updating inventory')

        elif 'disapprove' in request.POST:
            StokeTake.objects.filter(id=id).update(status='In Progress')
            messages.success(request, 'Stoke record sent back to stoke entry page')
        return redirect('inventory:list-stokes-for-approval')

    sub_context = {'title': "Approve Stoke Taking",
                   'stoke_form': stoke_obj, 'status': status, 'stoke_entries': entries}
    return render(request, 'approve-stoke.html', context=sub_context)


def delete_category_view(request, id):
    category = Category.objects.get(pk=id)
    deleted = category.delete()
    if deleted:
        messages.success(request, "Deleted Successfully")
    else:
        messages.error(request, "Error Not deleted")
    return redirect('inventory:list-categories')


def update_category_view(request, id):
    category = Category.objects.get(id=id)
    category_form = CategoryForm(instance=category, user=request.user)
    if request.method == 'POST':
        category_form = CategoryForm(request.POST, instance=category, user=request.user)
        if category_form.is_valid():
            category_obj = category_form.save(commit=False)
            category_obj.last_updated_by = request.user
            try:
                category_obj.save()
                if 'Save and exit' in request.POST:
                    return redirect('inventory:list-categories')
            except IntegrityError:
                messages.error(request, "Category name already exists")

    categoryContext = {
        'category_form': category_form,
        'title': 'Update Category',
        'update': True,

    }
    return render(request, 'create-category.html', context=categoryContext)


def create_uom_category(request):
    if request.method == 'POST':
        category_form = UomCategoryForm(request.POST)
        if category_form.is_valid():
            category_obj = category_form.save(commit=False)
            category_obj.company = request.user.company
            category_obj.created_by = request.user
            try:
                category_obj.save()
                messages.success(request, 'UOM Category created successfully')
            except IntegrityError:
                messages.error(request, 'UOM Category name already exists')
        else:
            messages.error(request, 'UOM Category NOT created')
    return redirect('inventory:list-uom-category')


def delete_uom_category(request, id):
    uom_category = UomCategory.objects.get(id=id)
    deleted = uom_category.delete()
    if deleted:
        messages.success(request, "Deleted Successfully")
    else:
        messages.error(request, "Error Not deleted")
    return redirect('inventory:list-uom-category')


def list_uom_category(request):
    uom_categories = UomCategory.objects.filter(company=request.user.company)
    # this form is for the modal used to create and update a record
    uom_category_form = UomCategoryForm()
    context = {"uom_category_list": uom_categories, 'category_from': uom_category_form}
    return render(request, 'list-uom-categories.html', context=context)


def update_uom_category(request, id):
    uom_category = UomCategory.objects.get(id=id)
    if request.method == 'POST':
        category_form = UomCategoryForm(request.POST, instance=uom_category)
        if category_form.is_valid():
            category_obj = category_form.save(commit=False)
            category_obj.last_updated_by = request.user
            try:
                category_obj.save()
            except IntegrityError:
                messages.error(request, 'UOM Category name already exists')
            messages.success(request, 'UOM Category updated successfully')
        else:
            messages.error(request, 'UOM Category NOT updated')
    return redirect('inventory:list-uom-category')


def check_balance_difference(stoke_take):
    stoke_entries = StokeEntry.objects.filter(stoke_take=stoke_take)
    result = []
    for stoke_entry in stoke_entries:
        item = stoke_entry.item
        location = stoke_entry.stoke_take.location
        on_hand_item = Inventory_Balance.objects.get(item=item, location=location)
        on_hand_quantity = on_hand_item.qnt
        stoked_quantity = stoke_entry.quantity
        difference_quantity = on_hand_quantity - stoked_quantity
        if difference_quantity > 0:
            result.append({'item': item, 'type': 'outbound', 'quantity': abs(difference_quantity), 'location': location})
        elif difference_quantity < 0:
            result.append({'item': item, 'type': 'inbound', 'quantity': abs(difference_quantity), 'location': location})

    return result


def create_stoke_transaction(stoke_take, user):
    result = check_balance_difference(stoke_take)
    if result:
        rows_number = MaterialTransaction1.objects.all().count()
        transaction_code = "STK-" + str(date.today()) + "-" + get_seq(rows_number)
        try:
            stoke_transaction = MaterialTransaction1(transaction_code=transaction_code, stoke_take=stoke_take,
                                                     date=date.today(), created_by=user, company=user.company)
            stoke_transaction.save()

            for record in result:
                item = record['item']
                t_type = record['type']
                quantity = record['quantity']
                location = record['location']
                new_line = MaterialTransactionLines(material_transaction=stoke_transaction, item=item,
                                                    transaction_type=t_type,
                                                    quantity=quantity, location=location, created_by=user)
                new_line.save()
            return True
        except BaseException as e:
            print(e)
            return False
    else:
        return True


def get_attribute_type(request, id):
    attribute = Attribute.objects.get(pk=id)
    serialized = AttributeSeializer(attribute)
    return JSONResponse(serialized.data, content_type='application/json')


def view_item(request, id):
    item = Item.objects.get(id=id)
    item_image = ItemImage.objects.filter(item=item)
    if len(item_image) != 0:
        item_image = item_image[0]
    attributes = ItemAttributeValue.objects.filter(item__id=id)
    subcontext = {
        'item': item,
        'attributes': attributes,
        'image': item_image,

    }
    return render(request, 'view-item.html', context=subcontext)


def update_item(request, id):
    item = Item.objects.get(id=id)
    try:
        item_image = ItemImage.objects.get(item=item)
    except ItemImage.DoesNotExist:
        item_image = None
    product = Product.objects.get(id=item.product.id)
    attribute_form = AttributeForm()
    image_form = ItemImageForm(instance=item_image)
    # attribute_value = ItemAttributeValue.objects.filter(item=item)
    product_form = ProductForm(instance=product, user=request.user)
    item_form = ItemForm(instance=item, user=request.user)
    item_attribute_form = item_attribute_model_formset(instance=item)
    for form in item_attribute_form:
        value = form.instance.value
        form.fields["temp_value"].initial = value
    if request.method == 'POST':
        product_form = ProductForm(
            request.POST, instance=product, user=request.user)
        item_form = ItemForm(request.POST, instance=item, user=request.user)
        item_attribute_form = item_attribute_model_formset(request.POST, instance=item)
        image_form = ItemImageForm(request.POST, request.FILES)
        if product_form.is_valid() and item_form.is_valid() and item_attribute_form.is_valid():
            product_obj = product_form.save(commit=False)
            product_obj.last_updated_by = request.user
            product_obj.save()
            item_obj = item_form.save(commit=False)
            item_obj.last_updated_by = request.user
            try:
                item_obj.save()
            except IntegrityError as e:
                messages.error(request , 'SKU must be unique')
                attributeContext = {
                    'title': "New Item",
                        'product_form': product_form,
                        'item_form': item_form,
                        'item_attribute_formset': item_attribute_form,
                        'attribute_form': attribute_form,
                        'image_form': image_form,
                        'item_image':item_image,

                }
                return render(request, 'create-product-item.html', context=attributeContext)
            image_obj = image_form.save(commit=False)
            image_obj.created_by = request.user
            image_obj.item = item_obj
            image_obj.save()
            item_attribute_form = item_attribute_model_formset(request.POST, instance=item_obj)
            if item_attribute_form.is_valid():
                for form in item_attribute_form:
                    temp_value = form.cleaned_data['temp_value']
                    att_obj = form.save(commit=False)
                    att_obj.value = temp_value
                    att_obj.last_updated_by = request.user
                    att_obj.save()

                if 'Save and exit' in request.POST:
                    return redirect('inventory:list-products')
                else:
                    return redirect('inventory:view-item', id=id)
        elif item_form.is_valid() == False:
            messages.error(request , item_form.errors)
    attributeContext = {
        'title': "Update Item",
        'product_form': product_form,
        'item_form': item_form,
        'item_attribute_formset': item_attribute_form,
        'attribute_form': attribute_form,
        'update': True,
        'image_form': image_form,
        'item_image':item_image,

    }
    return render(request, 'create-product-item.html', context=attributeContext)


def update_attribute(request, id):
    attribute = Attribute.objects.get(id=id)
    attribute_form = AttributeForm(instance=attribute)
    if request.method == 'POST':
        attribute_form = AttributeForm(request.POST, instance=attribute)
        if attribute_form.is_valid():
            attribute_obj = attribute_form.save(commit=False)
            attribute_obj.last_updated_by = request.user
            try:
                attribute_obj.save()
                if 'Save and exit' in request.POST:
                    return redirect('inventory:list-attributes')
            except IntegrityError:
                messages.error(request, "Attribute name and type already exit")

    attributeContext = {
        'attribute_form': attribute_form,
        'title': 'Update Attribute',
        'update': True,

    }
    return render(request, 'create-attribute.html', context=attributeContext)


def delete_attribute(request, id):
    attribute = Attribute.objects.get(id=id)
    try:
        attribute.delete()
    except ProtectedError:
        error_message = "This object can't be deleted!!"
        messages.error(request, error_message)
    return redirect('inventory:list-attributes')


def create_attribute_ajax(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        att_type = request.POST.get('att_type')

        response_data = {}
        try:
            attribute = Attribute(name=name, att_type=att_type, created_by=request.user,
                                  company=request.user.company)
            attribute.save()
            response_data['result'] = 'Create attribute successful!'
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        except ValidationError:
            return HttpResponse(
                json.dumps({"nothing to see": "this isn't happening"}),
                content_type="application/json"
            )
        # response_data['postpk'] = post.pk
        # response_data['text'] = post.text
        # response_data['created'] = post.created.strftime('%B %d, %Y %I:%M %p')
        # response_data['author'] = post.author.username


