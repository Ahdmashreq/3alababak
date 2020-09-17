from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from inventory.models import (Category, Brand, Product, Attribute, Item, Uom, StokeTake, StokeEntry, UomCategory)
from inventory.forms import (CategoryForm, category_model_formset, BrandForm, brand_model_formset,
                             AttributeForm, attribute_model_formset, ProductForm, product_item_inlineformset,
                             uom_formset, StokeTakeForm, UOMForm, stoke_entry_formset, StokeEntryForm, UomCategoryForm)


def create_category_view(request):
    category_form = CategoryForm()
    if request.method == 'POST':
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_obj = category_form.save(commit=False)
            category_obj.company = request.user.company
            category_obj.created_by = request.user
            category_obj.save()
            if 'Save and exit' in request.POST:
                return redirect('inventory:list-categories')
            elif 'Save and add' in request.POST:
                return redirect('inventory:create-category')

    categoryContext = {
        'category_form': category_form,
        'title': 'New Category'

    }
    return render(request, 'create-category.html', context=categoryContext)


def list_categorires_view(request):
    categories_list = Category.objects.all()
    categoryContext = {
        'categories_list': categories_list
    }
    return render(request, 'list-category.html', context=categoryContext)


def list_brands_view(request):
    brands_list = Brand.objects.all()
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
            brand_obj.save()
            if 'Save and exit' in request.POST:
                return redirect('inventory:list-brands')
            elif 'Save and add' in request.POST:
                return redirect('inventory:create-brand')

    categoryContext = {
        'brand_form': brand_form,
        'title': 'New Brand'

    }
    return render(request, 'create-brand.html', context=categoryContext)


def list_attributes_view(request):
    attributes_list = Attribute.objects.all()
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
            attribute_obj.save()
            if 'Save and exit' in request.POST:
                return redirect('inventory:list-attributes')
            elif 'Save and add' in request.POST:
                return redirect('inventory:create-attribute')

    attributeContext = {
        'attribute_form': attribute_form,
        'title': 'New Attribute'

    }
    return render(request, 'create-attribute.html', context=attributeContext)


def list_products_view(request):
    products_list = Product.objects.all()
    productsContext = {
        'products_list': products_list
    }
    return render(request, 'list-products.html', context=productsContext)


def create_product_item_view(request):
    product_form = ProductForm()
    item_formset = product_item_inlineformset(queryset=Item.objects.none())
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        item_formset = product_item_inlineformset(request.POST)
        if product_form.is_valid() and item_formset.is_valid():
            product_obj = product_form.save(commit=False)
            product_obj.company = request.user.company
            product_obj.created_by = request.user
            product_obj.save()
            item_formset = product_item_inlineformset(request.POST, instance=product_obj)
            if item_formset.is_valid():
                item_obj = item_formset.save(commit=False)
                for form in item_obj:
                    form.created_by = request.user
                    form.save()
                if 'Save and exit' in request.POST:
                    return redirect('inventory:list-products')
                elif 'Save and add' in request.POST:
                    return redirect('inventory:create-product')
    attributeContext = {
        'product_form': product_form,
        'item_formset': item_formset,

    }
    return render(request, 'create-product-item.html', context=attributeContext)


# def create_stoketake_view(request):
#     stoke_from = StokeTakeForm()
#     stoke_entry_inlineformset = stoke_entry_formset()
#     if request.method == 'POST':
#         stoke_form = StokeTakeForm(request.POST)
#         stoke_entry_inlineformset = stoke_entry_formset(request.POST)
#         if stoke_form.is_valid() and stoke_entry_inlineformset.is_valid():
#             stoke_obj = stoke_form.save(commit=False)
#             stoke_obj.created_by = request.user
#             stoke_obj.company = request.user.company
#             stoke_obj.save()
#             stoke_entry_inlineformset = stoke_entry_formset(request.POST, instance=stoke_obj)
#             if stoke_entry_inlineformset.is_valid():
#                 stoke_entry_obj = stoke_entry_inlineformset.save(commit=False)
#                 for stoke_entry in stoke_entry_obj:
#                     stoke_entry.created_by = request.user
#                     stoke_entry.save()
#                 if 'Save and exit' in request.POST:
#                     return redirect('inventory:list-stokes')
#                 elif 'Save and add' in request.POST:
#                     return redirect('inventory:create-stoke')
#             else:
#                 print(stoke_entry_inlineformset.errors)
#         else:
#             print(stoke_form.errors)
#     stoke_context = {
#         'stoke_form': stoke_from,
#         'stoke_entry_inlineformset': stoke_entry_inlineformset,
#         'title': 'New Stoke Take'
#
#     }
#     return render(request, 'create-stoke.html', context=stoke_context)


def list_stoketake_view(request):
    stoke_list = StokeTake.objects.all()
    stokes_context = {
        "title": "Stoke Takes",
        'stoke_list': stoke_list
    }
    return render(request, 'list-stokes.html', context=stokes_context)


def create_uom_view(request):
    uom_from = UOMForm()
    if request.method == 'POST':
        uom_from = UOMForm(request.POST)
        if uom_from.is_valid():
            uom_obj = uom_from.save(commit=False)
            uom_obj.created_by = request.user
            uom_obj.company = request.user.company
            uom_obj.save()
            if 'Save and exit' in request.POST:
                return redirect('inventory:list-uom')
            elif 'Save and add' in request.POST:
                return redirect('inventory:create-uom')
        else:
            print(uom_from.errors)
    uom_context = {
        'uom_from': uom_from,
        'title': 'New UOM'

    }
    return render(request, 'create-uom.html', context=uom_context)


def list_uom_view(request):
    uom_list = Uom.objects.all()
    uom_context = {
        'uom_list': uom_list
    }
    return render(request, 'list-uom.html', context=uom_context)


def create_stoke_take_template(request):
    print('Hi')
    # take the form values:name,type,date
    # get all records accoding to type
    # if category , it takes the value of cateogry and get all items under it
    # if location , it takes the value of location and get all items under it
    # design an html that has :
    # stoke name, stoke date, stoke type
    # a table for all items names , with a quatity columns an
    # if all is choosen add column for location or make it as a section
    # render it as pdf


def create_stoketake_view(request):
    stoke_from = StokeTakeForm(update=False)
    stoke_context = {}
    items = []
    if request.method == 'POST':
        stoke_form = StokeTakeForm(request.POST, update=False)
        if stoke_form.is_valid():
            stoke_obj = stoke_form.save(commit=False)
            stoke_obj.created_by = request.user
            stoke_obj.company = request.user.company
            name = stoke_obj.name
            date = stoke_obj.date
            type = stoke_obj.type
            stoke_context['name'] = name
            stoke_context['date'] = date
            stoke_context['type'] = type
            if type == 'location':
                location = stoke_obj.location
                items = Item.objects.filter(location=location)
                stoke_context['location'] = location
            elif type == 'category':
                category = stoke_obj.category
                descendants = Category.objects.get(name=category).get_descendants(include_self=True)
                products = Product.objects.filter(Q(category__parent__in=descendants) | Q(category__in=descendants))
                items = Item.objects.filter(product__in=products)
                stoke_context['category'] = category
            elif type == 'all':
                items = Item.objects.all()
            elif type == 'random':
                pass

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
            print(stoke_from.errors)

    stoke_context = {
        'stoke_form': stoke_from,
        'title': 'New Stoke Take'

    }
    return render(request, 'create-stoke.html', context=stoke_context)


def update_stoke_take_view(request, id):
    stoke_inst = StokeTake.objects.get(id=id)
    stoke_form = StokeTakeForm(update=False, instance=stoke_inst)

    if request.method == 'POST':
        stoke_form = StokeTakeForm(request.POST, update=False, instance=stoke_inst)
        if stoke_form.is_valid():
            stoke_obj = stoke_form.save(commit=False)
            stoke_obj.updated_by = request.user
            if stoke_obj.type == 'location':
                stoke_obj.category = None
                items = Item.objects.filter(location=stoke_obj.location)
            elif stoke_obj.type == 'category':
                stoke_obj.location = None
                category = stoke_obj.category
                descendants = Category.objects.get(name=category).get_descendants(include_self=True)
                products = Product.objects.filter(Q(category__parent__in=descendants) | Q(category__in=descendants))
                items = Item.objects.filter(product__in=products)
            elif stoke_obj.type == 'all':
                stoke_obj.location = None
                stoke_obj.category = None
                items = Item.objects.all()

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

    context = {'stoke_form': stoke_form, 'title': 'Update Stoke'}
    return render(request, 'create-stoke.html', context=context)


def list_stoketake_entries(request):
    stoke_list = StokeTake.objects.exclude(status='Approved')
    context = {"title": "Stoke Take Entries", "entry_mode": True, 'stoke_list': stoke_list}

    return render(request, 'list-stokes.html', context=context)


def update_stoke_entry_view(request, id):
    stoke_obj = StokeTake.objects.get(id=id)
    stoke_take_form = StokeTakeForm(update=True, instance=stoke_obj)
    stoke_entry_inline_formset = stoke_entry_formset(instance=stoke_obj, form_kwargs={'approve': False})

    if request.method == 'POST':
        stoke_entry_inline_formset = stoke_entry_formset(request.POST, instance=stoke_obj,
                                                         form_kwargs={'approve': False})
        if stoke_entry_inline_formset.is_valid():
            stoke_entry_obj = stoke_entry_inline_formset.save(commit=False)
            for stoke_entry in stoke_entry_obj:
                stoke_entry.last_updated_by = request.user
                stoke_entry.save()

            if len(StokeEntry.objects.filter(stoke_take=stoke_obj, quantity=None)) == 0:
                stoke_obj.status = 'Pending Approval'
                stoke_obj.save()
            elif len(StokeEntry.objects.filter(stoke_take=stoke_obj).exclude(quantity=None)) > 0:
                stoke_obj.status = 'In Progress'
                stoke_obj.save()
            else:
                stoke_obj.status = 'Drafted'
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
    stoke_context['name'] = name
    stoke_context['date'] = date
    stoke_context['type'] = type
    if type == 'location':
        location = stoke_obj.location
        items = Item.objects.filter(location=location)
        stoke_context['location'] = location
    elif type == 'category':
        category = stoke_obj.category
        descendants = Category.objects.get(name=category).get_descendants(include_self=True)
        products = Product.objects.filter(Q(category__parent__in=descendants) | Q(category__in=descendants))
        items = Item.objects.filter(product__in=products)
        stoke_context['category'] = category
    elif type == 'all':
        items = Item.objects.all()
    elif type == 'random':
        pass
    stoke_context['items'] = items
    return render(request, 'stoke-entry-template.html', context=stoke_context)


def list_stoketake_approvals(request):
    stoke_list = StokeTake.objects.filter(Q(status='Pending Approval') | Q(status='Approved'))
    context = {"entry_mode": True, 'stoke_list': stoke_list}
    return render(request, 'list-stoke-approvals.html', context=context)


def approve_stoke_view(request, id):
    stoke_obj = StokeTake.objects.get(id=id)
    stoke_take_form = StokeTakeForm(update=True, instance=stoke_obj)
    stoke_entry_inline_formset = stoke_entry_formset(instance=stoke_obj, form_kwargs={'approve': True})

    if request.method == 'POST':
        stoke_entry_inline_formset = stoke_entry_formset(request.POST, instance=stoke_obj,
                                                         form_kwargs={'approve': True})
        if stoke_entry_inline_formset.is_valid():
            stoke_entry_obj = stoke_entry_inline_formset.save(commit=False)
            for stoke_entry in stoke_entry_obj:
                stoke_entry.last_updated_by = request.user
                stoke_entry.save()
            if len(StokeEntry.objects.filter(stoke_take=stoke_obj, approval=False)) == 0:
                stoke_obj.status = 'Approved'
                stoke_obj.save()
            elif len(StokeEntry.objects.filter(stoke_take=stoke_obj, approval=False)) > 0:
                stoke_obj.status = 'Pending Approval'
                stoke_obj.save()
            if 'Save and exit' in request.POST:
                return redirect('inventory:list-stokes-for-approval')

    sub_context = {'title': "Approve Stoke", 'stoke_entry_inlineformset': stoke_entry_inline_formset,
                   'stoke_form': stoke_take_form}
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
    category_form = CategoryForm(instance=category)
    if request.method == 'POST':
        category_form = CategoryForm(request.POST, instance=category)
        if category_form.is_valid():
            category_obj = category_form.save(commit=False)
            category_obj.last_updated_by = request.user
            category_obj.save()
            if 'Save and exit' in request.POST:
                return redirect('inventory:list-categories')

    categoryContext = {
        'category_form': category_form,
        'title': 'Update Category',
        'update': True,

    }
    return render(request, 'create-category.html', context=categoryContext)


def create_uom_category(request):
    category_form = UomCategoryForm()
    uom_categories = UomCategory.objects.all()
    if request.method == 'POST':
        category_form = UomCategoryForm(request.POST)
        if category_form.is_valid():
            category_obj = category_form.save(commit=False)
            category_obj.company = request.user.company
            category_obj.created_by = request.user
            category_obj.save()
            messages.success(request, 'UOM Category created successfully')
            uom_categories = UomCategory.objects.all()
        else:
            messages.error(request, 'UOM Category NOT created')
    context = {'category_from': category_form,"uom_category_list": uom_categories}
    return redirect('inventory:list-uom-category')


def list_uom_category(request):
    uom_categories = UomCategory.objects.all()
    print(uom_categories)
    uom_category_form = UomCategoryForm()
    context = {"uom_category_list": uom_categories, 'category_from': uom_category_form}
    return render(request,'list-uom-categories.html', context=context)
