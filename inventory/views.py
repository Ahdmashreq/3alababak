from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from inventory.models import (Category, Brand, Product, Attribute, Item, Uom, StokeTake, StokeEntry)
from inventory.forms import (CategoryForm, category_model_formset, BrandForm, brand_model_formset,
                             AttributeForm, attribute_model_formset, ProductForm, product_item_inlineformset,
                             uom_formset, StokeTakeForm)


def create_category_view(request):
    category_formset = category_model_formset(queryset=Category.objects.none())
    if request.method == 'POST':
        category_formset = category_model_formset(request.POST)
        if category_formset.is_valid():
            category_obj = category_formset.save(commit=False)
            for form in category_obj:
                form.company = request.user.company
                form.created_by = request.user
                form.save()
            return redirect('inventory:list-categories')
    categoryContext = {
        'category_formset': category_formset,
        'title': 'New Category'

    }
    return render(request, 'create-category.html', context=categoryContext)


def list_categorires_view(request):
    categories_list = Category.objects.all()
    categoryContext = {
        'categories_list': categories_list
    }
    return render(request, 'list-categories.html', context=categoryContext)


def list_brands_view(request):
    brands_list = Brand.objects.all()
    brandsContext = {
        'brands_list': brands_list
    }
    return render(request, 'list-brands.html', context=brandsContext)


def create_brand_view(request):
    brand_formset = brand_model_formset(queryset=Brand.objects.none())
    if request.method == 'POST':
        brand_formset = brand_model_formset(request.POST)
        if brand_formset.is_valid():
            brand_obj = brand_formset.save(commit=False)
            for form in brand_obj:
                form.company = request.user.company
                form.created_by = request.user
                form.save()
            return redirect('inventory:list-brands')
    categoryContext = {
        'brand_formset': brand_formset,
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
    attribute_formset = attribute_model_formset(queryset=Attribute.objects.none())
    if request.method == 'POST':
        attribute_formset = attribute_model_formset(request.POST)
        if attribute_formset.is_valid():
            attribute_obj = attribute_formset.save(commit=False)
            for form in attribute_obj:
                form.company = request.user.company
                form.created_by = request.user
                form.save()
            return redirect('inventory:list-attributes')
    attributeContext = {
        'attribute_formset': attribute_formset,
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
            return redirect('inventory:list-products')
    attributeContext = {
        'product_form': product_form,
        'item_formset': item_formset,

    }
    return render(request, 'create-product-item.html', context=attributeContext)


def list_stoketake_view(request):
    stoke_list = StokeTake.objects.all()
    stokes_context = {
        'stoke_list': stoke_list
    }
    return render(request, 'list-stokes.html', context=stokes_context)


def create_uom_view(request):
    uom_from = uom_formset(queryset=Uom.objects.none())
    if request.method == 'POST':
        uom_from = uom_formset(request.POST)
        if uom_from.is_valid():
            uom_obj = uom_from.save(commit=False)
            for uom in uom_obj:
                uom.created_by = request.user
                uom.company = request.user.company
                uom.save()
            return redirect("inventory:list-uom")
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
    stoke_from = StokeTakeForm()
    stoke_context = {}
    items = []
    if request.method == 'POST':

        stoke_form = StokeTakeForm(request.POST)
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
                items = Product.objects.filter(Q(category__parent__in=descendants) | Q(category__in=descendants))
                # items = Product.objects.filter(category=category)
                stoke_context['category'] = category
            elif type == 'all':
                items = Item.objects.all()
            elif type == 'random':
                pass

            stoke_obj.save()
            entry_list = []
            for item in items:
                entry_list.append(StokeEntry(stoke_take=stoke_obj, item=item))
            StokeEntry.objects.bulk_create(entry_list)
            print("****************8")
            print(StokeEntry.objects.all())
            stoke_context['items'] = items
            return render(request, 'stoke-entry-template.html', context=stoke_context)

        else:
            print(stoke_form.errors)
    stoke_context = {
        'stoke_form': stoke_from,
        'title': 'New Stoke Take'

    }
    return render(request, 'create-stoke.html', context=stoke_context)


def update_stoke_entry_view(request, id):
    stoke_obj = StokeTake.objects.get(id=id)
    stoke_take_form = StokeTakeForm(update=True,instance=stoke_obj)
    stoke_entries = StokeEntry.objects.filter(stoke_take=stoke_obj)
    sub_context = {'title':"Update Stoke Entry",'stoke_entries': stoke_entries, 'stoke_form': stoke_take_form}
    return render(request,'update-stoke.html',context=sub_context)
