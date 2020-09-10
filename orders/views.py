from django.shortcuts import render, redirect
from orders.forms import (PurchaseTransactionCreationForm,
                          PurchaseOrderCreationForm,
                          purchase_transaction_formset,
                          sale_transaction_formset,
                          SaleOrderCreationForm)
from orders.models import PurchaseOder, SalesOrder
from inventory.models import Item
from django.contrib import messages
from json import dumps
from rest_framework import serializers
# from django.core import serializers
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import json
from dal import autocomplete


def create_purchase_order_view(request):
    po_form = PurchaseOrderCreationForm()
    po_transaction_inlineformset = purchase_transaction_formset()
    print("************88888")
    print(po_transaction_inlineformset[0].fields['total_price'].fields[0])
    # filter = PoFilter(request.GET, queryset=Item.objects.all())
    if request.method == 'POST':
        po_form = PurchaseOrderCreationForm(request.POST)
        po_transaction_inlineformset = purchase_transaction_formset(request.POST)
        if po_form.is_valid() and po_transaction_inlineformset.is_valid():
            po_obj = po_form.save(commit=False)
            po_obj.created_by = request.user
            po_obj.company = request.user.company
            po_obj.save()

            po_transaction_inlineformset = purchase_transaction_formset(request.POST, instance=po_obj)
            if po_transaction_inlineformset.is_valid():
                po_transaction_obj = po_transaction_inlineformset.save(commit=False)
                for po_transaction in po_transaction_obj:
                    po_transaction.created_by = request.user
                    po_transaction.save()
                messages.success(request, 'Saved Successfully')
                if 'Save and exit' in request.POST:
                    return redirect('orders:list-po')
                elif 'Save and add' in request.POST:
                    return redirect('orders:create-po')
            else:
                print("************")
                print(po_transaction_inlineformset.errors)
        else:
            print("))))))))))))))))")
            print(po_form.errors)
            print(po_transaction_inlineformset.errors)
    items = Item.objects.all()
    subcontext = {
        'po_form': po_form,
        'po_transaction_inlineformset': po_transaction_inlineformset,
        'items': items,
        # 'filter': filter,
        'title': 'New Purchase Order',
    }
    return render(request, 'create-purchase-order.html', context=subcontext)


def list_purchase_order_view(request):
    purchase_orders = PurchaseOder.objects.all()
    subcontext = {
        'purchase_orders_list': purchase_orders
    }
    return render(request, 'list-purchase_orders.html', context=subcontext)


def update_purchase_order_view(request, id):
    order = PurchaseOder.objects.get(pk=id)
    purchase_order_form = PurchaseOrderCreationForm(instance=order)
    po_transaction_inlineformset = purchase_transaction_formset(instance=order)
    if request.method == 'POST':
        purchase_order_form = PurchaseOrderCreationForm(request.POST, instance=order)
        po_transaction_inlineformset = purchase_transaction_formset(request.POST, instance=order)
        if purchase_order_form.is_valid() and po_transaction_inlineformset.is_valid():
            po_obj = purchase_order_form.save(commit=False)
            po_obj.last_updated_by = request.user
            po_instance = po_obj.save()
            po_transaction_inlineformset = purchase_transaction_formset(request.POST, instance=po_instance)
            if po_transaction_inlineformset.is_valid():
                po_transaction_obj = po_transaction_inlineformset.save(commit=False)
                for po_transaction in po_transaction_obj:
                    po_transaction.last_updated_by = request.user
                    po_transaction.save()
                messages.success(request, 'Saved Successfully')
                return redirect('orders:list-po')
            else:
                print(po_transaction_inlineformset.errors)
        else:
            print(purchase_order_form.errors)

    supContext = {
        'po_form': purchase_order_form,
        'po_transaction_inlineformset': po_transaction_inlineformset,
        'title': 'Update Purchase Order'

    }
    return render(request, 'create-purchase-order.html', supContext)


def delete_purchase_order_view(request, id):
    po_order = PurchaseOder.objects.get(pk=id)
    deleted = po_order.delete()
    if deleted:
        return redirect('orders:list-po')
    else:
        print("item not deleted")


def create_sales_order_view(request):
    so_form = SaleOrderCreationForm()
    so_transaction_inlineformset = sale_transaction_formset()
    if request.method == 'POST':
        so_form = SaleOrderCreationForm(request.POST)
        so_transaction_inlineformset = sale_transaction_formset(request.POST)
        if so_form.is_valid() and so_transaction_inlineformset.is_valid():
            so_obj = so_form.save(commit=False)
            so_obj.created_by = request.user
            so_obj.company = request.user.company
            so_instance = so_obj.save()
            so_transaction_inlineformset = sale_transaction_formset(request.POST, instance=so_instance)
            if so_transaction_inlineformset.is_valid():
                so_transaction_obj = so_transaction_inlineformset.save(commit=False)
                for so_transaction in so_transaction_obj:
                    so_transaction.created_by = request.user
                    so_transaction.save()
                messages.success(request, 'Saved Successfully')
                if 'Save and exit' in request.POST:
                    return redirect('orders:list-so')
                elif 'Save and add' in request.POST:
                    return redirect('orders:create-so')
            else:
                print(so_transaction_inlineformset.errors)
        else:
            print(so_form.errors)
    subcontext = {
        'so_form': so_form,
        'so_transaction_inlineformset': so_transaction_inlineformset,
        'title': 'New Sale Order'

    }
    return render(request, 'create-sale-order.html', context=subcontext)


def list_sale_order_view(request):
    sale_orders = SalesOrder.objects.all()
    subcontext = {
        'sale_orders_list': sale_orders
    }
    return render(request, 'list-sale_orders.html', context=subcontext)


def update_sale_order_view(request, id):
    order = SalesOrder.objects.get(pk=id)
    sale_order_form = SaleOrderCreationForm(instance=order)
    so_transaction_inlineformset = sale_transaction_formset(instance=order)
    if request.method == 'POST':
        sale_order_form = SaleOrderCreationForm(request.POST, instance=order)
        so_transaction_inlineformset = sale_transaction_formset(request.POST, instance=order)
        if sale_order_form.is_valid() and so_transaction_inlineformset.is_valid():
            so_obj = sale_order_form.save(commit=False)
            so_obj.last_updated_by = request.user
            so_instance = so_obj.save()
            so_transaction_inlineformset = sale_transaction_formset(request.POST, instance=so_instance)
            if so_transaction_inlineformset.is_valid():
                so_transaction_obj = so_transaction_inlineformset.save(commit=False)
                for so_transaction in so_transaction_obj:
                    so_transaction.last_updated_by = request.user
                    so_transaction.save()
                messages.success(request, 'Saved Successfully')
                return redirect('orders:list-so')
            else:
                print(so_transaction_inlineformset.errors)
        else:
            print(sale_order_form.errors)

    supContext = {
        'so_form': sale_order_form,
        'so_transaction_inlineformset': so_transaction_inlineformset,
        'title': 'Update Sale Order'

    }
    return render(request, 'create-sale-order.html', supContext)


def delete_sale_order_view(request, id):
    so_order = SalesOrder.objects.get(pk=id)
    deleted = so_order.delete()
    if deleted:
        return redirect('orders:list-so')
    else:
        print("item not deleted")


class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class ItemSerializer(serializers.ModelSerializer):
    uom = serializers.StringRelatedField(many=False)

    class Meta:
        model = Item
        fields = ('avg_cost', 'uom',)


def get_item(request, id):
    item = Item.objects.select_related().get(pk=id)
    serialized = ItemSerializer(item)
    return JSONResponse(serialized.data, content_type='application/json')


class ItemAutocomplete(autocomplete.Select2QuerySetView):
    print("inside ItemAutocomplete")

    def get_queryset(self):
        print("inside get_queryset ItemAutocomplete")
        if not self.request.user.is_authenticated:
            return Item.objects.none()
        qs = Item.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
