from django.shortcuts import render, redirect
from django.contrib import messages
from inventory.models import (Category, Brand, Product, Attribute, Item, Uom, StokeTake)
from inventory.forms import (CategoryForm, category_model_formset, BrandForm, brand_model_formset,
                             AttributeForm, attribute_model_formset, ProductForm, product_item_inlineformset,
                             stoke_entry_formset, uom_formset, StokeTakeForm,UOMForm)


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
    return render(request, 'list-categories.html', context=categoryContext)


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


def create_stoketake_view(request):
    stoke_from = StokeTakeForm()
    stoke_entry_inlineformset = stoke_entry_formset()
    if request.method == 'POST':
        stoke_form = StokeTakeForm(request.POST)
        stoke_entry_inlineformset = stoke_entry_formset(request.POST)
        if stoke_form.is_valid() and stoke_entry_inlineformset.is_valid():
            stoke_obj = stoke_form.save(commit=False)
            stoke_obj.created_by = request.user
            stoke_obj.company = request.user.company
            stoke_obj.save()
            stoke_entry_inlineformset = stoke_entry_formset(request.POST, instance=stoke_obj)
            if stoke_entry_inlineformset.is_valid():
                stoke_entry_obj = stoke_entry_inlineformset.save(commit=False)
                for stoke_entry in stoke_entry_obj:
                    stoke_entry.created_by = request.user
                    stoke_entry.save()
                if 'Save and exit' in request.POST:
                    return redirect('inventory:list-stokes')
                elif 'Save and add' in request.POST:
                    return redirect('inventory:create-stoke')
            else:
                print(stoke_entry_inlineformset.errors)
        else:
            print(stoke_form.errors)
    stoke_context = {
        'stoke_form': stoke_from,
        'stoke_entry_inlineformset': stoke_entry_inlineformset,
        'title': 'New Stoke Take'

    }
    return render(request, 'create-stoke.html', context=stoke_context)


def list_stoketake_view(request):
    stoke_list = StokeTake.objects.all()
    stokes_context = {
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
