from datetime import date

from django.db.models import Q
from django.shortcuts import render, redirect
from orders.forms import (PurchaseTransactionCreationForm,
                          PurchaseOrderCreationForm, ReceivingTransactionCreation_formset,
                          purchase_transaction_formset,
                          sale_transaction_formset,
                          SaleOrderCreationForm, MaterialTransactionCreationForm, MaterialTransactionLinesCreationForm,
                          MaterialTransactionCreation_formset)
from orders.models import PurchaseOder, SalesOrder, MaterialTransaction, PurchaseTransaction, MaterialTransactionLines, \
    MaterialTransaction1
from inventory.models import Item, Uom
from django.contrib import messages
from json import dumps
from rest_framework import serializers
# from django.core import serializers
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import json
from dal import autocomplete
from moneyed import Money, EGP
import random
from orders.utils import get_seq


def create_purchase_order_view(request):
    po_form = PurchaseOrderCreationForm()
    po_transaction_inlineformset = purchase_transaction_formset()
    rows_number = PurchaseOder.objects.all().count()
    po_code = "PO-" + str(date.today()) + "-" + get_seq(rows_number)
    po_form.fields['purchase_code'].initial = po_code
    if request.method == 'POST':
        po_form = PurchaseOrderCreationForm(request.POST)
        po_transaction_inlineformset = purchase_transaction_formset(request.POST)
        if po_form.is_valid() and po_transaction_inlineformset.is_valid():
            po_obj = po_form.save(commit=False)
            # po_obj.global_price = Money(str(po_form.cleaned_data['my_global_price']), EGP)
            po_obj.created_by = request.user
            po_obj.company = request.user.company
            po_obj.purchase_code = po_code
            if 'Save as draft' in request.POST:
                po_obj.status = "drafted"
            po_obj.save()
            po_transaction_inlineformset = purchase_transaction_formset(request.POST, instance=po_obj)
            if po_transaction_inlineformset.is_valid():
                for form in po_transaction_inlineformset:
                    po_transaction_obj = form.save(commit=False)
                    po_transaction_obj.created_by = request.user
                    po_transaction_obj.balance = po_transaction_obj.quantity
                    # po_transaction_obj.price_per_unit = Money(str(form.cleaned_data['my_price_per_unit']), EGP)
                    if po_obj.discount_type == "percentage":
                        po_transaction_obj.discount_percentage = po_obj.discount
                    elif po_obj.discount_type == "amount":
                        # TODO: implement this if
                        po_transaction_obj.discount_percentage = po_obj.discount

                    po_transaction_obj.save()
                    # po_transaction_obj = po_transaction_inlineformset.save(commit=False)
                # for po_transaction in po_transaction_obj:
                #     po_transaction.created_by = request.user
                #     po_transaction.save()
                messages.success(request, 'Saved Successfully')
                if 'Save and exit' in request.POST:
                    return redirect('orders:list-po')

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
        'title': 'New Purchase Order',
    }

    return render(request, 'create-purchase-order.html', context=subcontext)


def list_purchase_order_view(request):
    purchase_orders = PurchaseOder.objects.all()
    subcontext = {
        'purchase_orders_list': purchase_orders,
        'title': "Purchase Orders",
    }
    return render(request, 'list-purchase_orders.html', context=subcontext)


def update_purchase_order_view(request, id):
    order = PurchaseOder.objects.get(pk=id)
    purchase_order_form = PurchaseOrderCreationForm(instance=order)
    po_transaction_inlineformset = purchase_transaction_formset(instance=order)
    purchase_order_form.fields["my_total_price_after_discount"].initial = order.global_price_after_discount
    for form in po_transaction_inlineformset:
        item = form.instance.item
        uom = item.uom
        unit_price = item.avg_cost.amount
        form.fields["temp_uom"].initial = uom
        form.fields["price_per_unit"].initial = unit_price
        form.fields["after_discount"].initial = form.instance.total_price_after_discount

    if request.method == 'POST':
        purchase_order_form = PurchaseOrderCreationForm(request.POST, instance=order)
        po_transaction_inlineformset = purchase_transaction_formset(request.POST, instance=order)
        if purchase_order_form.is_valid() and po_transaction_inlineformset.is_valid():
            po_obj = purchase_order_form.save(commit=False)
            po_obj.last_updated_by = request.user
            if 'Save as open' in request.POST:
                po_obj.status = 'open'
            po_obj.save()
            po_transaction_inlineformset = purchase_transaction_formset(request.POST, instance=po_obj)
            if po_transaction_inlineformset.is_valid():
                for form in po_transaction_inlineformset:
                    po_transaction_obj = form.save(commit=False)
                    po_transaction_obj.last_updated_by = request.user
                    if po_obj.discount_type == "percentage":
                        po_transaction_obj.discount_percentage = po_obj.discount
                    elif po_obj.discount_type == "amount":
                        # TODO: implement this if
                        po_transaction_obj.discount_percentage = po_obj.discount
                    po_transaction_obj.save()
                messages.success(request, 'Saved Successfully')
                if 'Save and exit' in request.POST:
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
    return render(request, 'update-purchase-order.html', supContext)


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
            so_obj.save()
            so_transaction_inlineformset = sale_transaction_formset(request.POST, instance=so_obj)
            if so_transaction_inlineformset.is_valid():
                so_transaction_obj = so_transaction_inlineformset.save(commit=False)
                for so_transaction in so_transaction_obj:
                    so_transaction.created_by = request.user
                    so_transaction.save()
                messages.success(request, 'Saved Successfully')
                if 'Save and exit' in request.POST:
                    return redirect('orders:list-so')

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
    for form in so_transaction_inlineformset:
        print(form.instance.item.id)
        item = form.instance.item
        uom = item.uom

        unit_price = item.avg_cost.amount
        print(unit_price)
        form.fields["temp_uom"].initial = uom
        form.fields["price_per_unit"].initial = unit_price
    if request.method == 'POST':
        sale_order_form = SaleOrderCreationForm(request.POST, instance=order)
        so_transaction_inlineformset = sale_transaction_formset(request.POST, instance=order)
        if sale_order_form.is_valid() and so_transaction_inlineformset.is_valid():
            so_obj = sale_order_form.save(commit=False)
            so_obj.last_updated_by = request.user
            so_obj.save()
            so_transaction_inlineformset = sale_transaction_formset(request.POST, instance=so_obj)
            if so_transaction_inlineformset.is_valid():
                so_transaction_obj = so_transaction_inlineformset.save(commit=False)
                for so_transaction in so_transaction_obj:
                    so_transaction.last_updated_by = request.user
                    so_transaction.save()
                messages.success(request, 'Updated Successfully')
                if 'Save and exit' in request.POST:
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
        fields = ('uom',)


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


class PoItemAutocomplete(autocomplete.Select2QuerySetView):
    print("inside ItemAutocomplete")

    def get_queryset(self):
        print("inside get_queryset ItemAutocomplete")
        print("HIIIIIIIIIII")
        if not self.request.user.is_authenticated:
            return Item.objects.none()
        qs = Item.objects.all()
        po = self.forwarded.get('purchase_order', None)
        print(po)
        # items = PurchaseTransaction.objects.filter(purchase_order=po, status='open').values(['item'])
        # #print("HIIIIIIIIIII")
        # print(items)
        # items = [po.item for po in purchase_transactions]

        # qs = items
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


def list_purchases_for_receiving(request):
    purchase_orders = PurchaseOder.objects.filter(~Q(status='drafted'))
    subcontext = {
        'purchase_orders_list': purchase_orders,
        'receiving': True,
        'title': "Purchase Orders Transactions",

    }
    return render(request, 'list-purchase_orders.html', context=subcontext)


def list_receiving(request, id):
    receivings = MaterialTransaction1.objects.filter(purchase_order__id=id)
    po = PurchaseOder.objects.get(id=id)
    status = po.status
    subcontext = {
        'pk': id,
        'receivings': receivings,
        'status': status,

    }
    return render(request, 'list-receiving.html', context=subcontext)


def create_receiving(request, id):
    receiving_formset = ReceivingTransactionCreation_formset(form_kwargs={'id': id})
    purchase_lines = PurchaseTransaction.objects.filter(purchase_order__id=id)
    purchase_order = PurchaseOder.objects.get(id=id)

    if request.method == 'POST':
        receiving_formset = ReceivingTransactionCreation_formset(request.POST, instance=purchase_order,
                                                                 form_kwargs={'id': id})
        if receiving_formset.is_valid():
            receiving_objs = receiving_formset.save(commit=False)
            transaction_code = "REC-" + str(date.today()) + "-" + str(random.randint(0, 5000))
            for obj in receiving_objs:
                obj.created_by = request.user
                obj.transaction_type = 'in'
                obj.transaction_code = transaction_code
                obj.save()
                po_line = PurchaseTransaction.objects.filter(purchase_order__id=id, item=obj.item)
                new_balance = po_line[0].balance - obj.quantity
                if new_balance == 0:
                    PurchaseTransaction.objects.filter(purchase_order__id=id, item=obj.item).update(balance=new_balance,
                                                                                                    status='closed')
                else:
                    PurchaseTransaction.objects.filter(purchase_order__id=id, item=obj.item).update(balance=new_balance)
            purchase_lines = PurchaseTransaction.objects.filter(purchase_order__id=id)
            flag = False
            for line in purchase_lines:
                if line.status == 'open' or line.status == 'Partial_receive':
                    flag = True
                    break
            if not flag:
                PurchaseOder.objects.filter(id=id).update(status='closed')
            else:
                PurchaseOder.objects.filter(id=id).update(status='Partially Received')
            if 'Save and exit' in request.POST:
                return redirect('orders:list-receiving', id=id)
        else:
            print(receiving_formset.errors)

    subcontext = {
        'po': purchase_order,
        'receiving_form': receiving_formset,
        'purchase_lines': purchase_lines,

    }
    return render(request, 'create-receiving.html', context=subcontext)




def create_receiving2(request, id):
    material_form = MaterialTransactionCreationForm()
    material_lines_formset = MaterialTransactionCreation_formset(form_kwargs={'id': id})
    purchase_lines = PurchaseTransaction.objects.filter(purchase_order__id=id)
    purchase_order = PurchaseOder.objects.get(id=id)
    rows_number = MaterialTransaction1.objects.all().count()
    transaction_code = "REC-" + str(date.today()) + "-" + get_seq(rows_number)
    material_form.fields["transaction_code"].initial = transaction_code

    if request.method == 'POST':
        material_form = MaterialTransactionCreationForm(request.POST)
        if material_form.is_valid():
            material_obj = material_form.save(commit=False)
            material_obj.purchase_order = purchase_order
            material_obj.transaction_code = transaction_code
            material_obj.created_by = request.user
            material_obj.save()
            material_lines_formset = MaterialTransactionCreation_formset(request.POST, instance=material_obj,
                                                                         form_kwargs={'id': id})
        if material_lines_formset.is_valid():
            receiving_objs = material_lines_formset.save(commit=False)
            for obj in receiving_objs:
                obj.created_by = request.user
                obj.transaction_type = 'in'
                obj.save()
                po_line = PurchaseTransaction.objects.filter(purchase_order__id=id, item=obj.item)
                new_balance = po_line[0].balance - obj.quantity
                if new_balance == 0:
                    PurchaseTransaction.objects.filter(purchase_order__id=id, item=obj.item).update(balance=new_balance,
                                                                                                    status='closed')
                else:
                    PurchaseTransaction.objects.filter(purchase_order__id=id, item=obj.item).update(balance=new_balance)
            purchase_lines = PurchaseTransaction.objects.filter(purchase_order__id=id)
            flag = False
            for line in purchase_lines:
                if line.status == 'open' or line.status == 'Partial_receive':
                    flag = True
                    break
            if not flag:
                PurchaseOder.objects.filter(id=id).update(status='closed')
            else:
                PurchaseOder.objects.filter(id=id).update(status='Partially Received')
            if 'Save and exit' in request.POST:
                return redirect('orders:list-receiving', id=id)
        else:
            print(material_form.errors)
            print(material_lines_formset.errors)

    subcontext = {
        'po': purchase_order,
        'transaction_form': material_form,
        'transaction_lines_form': material_lines_formset,
        'purchase_lines': purchase_lines,

    }
    return render(request, 'create-receiving_test.html', context=subcontext)


def view_received(request, id):
    material_transaction = MaterialTransaction1.objects.get(id=id)
    receiving_lines = MaterialTransactionLines.objects.filter(material_transaction=material_transaction)
    purchase_order = material_transaction.purchase_order

    subcontext = {
        'po': purchase_order,
        'material_transaction': material_transaction,
        'receiving_lines': receiving_lines,

    }
    return render(request, 'view-receiving.html', context=subcontext)


def view_purchase_order(request, id,flag):
    purchase_order = PurchaseOder.objects.get(id=id)
    purchase_lines = PurchaseTransaction.objects.filter(purchase_order__id=id)
    print("HERE IS MY FLag",flag)
    subcontext = {
        'po': purchase_order,
        'po_lines': purchase_lines,
        'flag':flag,

    }
    return render(request, 'view-po.html', context=subcontext)
