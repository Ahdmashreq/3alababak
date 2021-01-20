from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, ProtectedError
from django.shortcuts import render, redirect
from django.contrib import messages

from dal import autocomplete
from datetime import date
from decimal import Decimal 

from orders.forms import (PurchaseOrderCreationForm,
                          purchase_transaction_formset,
                          sale_transaction_formset,
                          SaleOrderCreationForm, MaterialTransactionCreationForm,
                          MaterialTransactionCreation_formset, TaxForm)
from orders.models import PurchaseOder, SalesOrder, PurchaseTransaction, MaterialTransactionLines, \
    MaterialTransaction1, Inventory_Balance, SalesTransaction, Tax
from inventory.models import Item, Uom
from orders.utils import get_seq, ItemSerializer, JSONResponse


def create_purchase_order_view(request):
    """
        Create a purchase order :model:`Orders.PurchaseOrder`.

        **Context**

        ``po_form``
            An instance of :form:`Orders.forms.PurchaseOrderCreationForm`.
        ``po_transaction_inlineformset``
            An instance of :inlineformset_factory:`Orders.forms.purchase_transaction_formset`
        ``title``
            A string representing the title of the rendered HTML page

        **Template:**

        :template:`orders/templates/create-purchase-order.html`

    """
    po_form = PurchaseOrderCreationForm(user=request.user)
    po_transaction_inlineformset = purchase_transaction_formset(form_kwargs={'user': request.user})
    rows_number = PurchaseOder.objects.filter(company=request.user.company).count()
    po_code = "PO-" + get_seq(rows_number)
    try:
        tax = Tax.objects.get(name='VAT')
        tax_percentage = tax.value / 100
    except ObjectDoesNotExist:
        print(ObjectDoesNotExist)
        tax_percentage = Decimal(0.14)
    po_form.fields['tax'].initial = round(tax_percentage, 2)
    po_form.fields['purchase_code'].initial = po_code
    if request.method == 'POST':
        po_form = PurchaseOrderCreationForm(request.POST, user=request.user)
        po_transaction_inlineformset = purchase_transaction_formset(request.POST, form_kwargs={'user': request.user})
        if po_form.is_valid() and po_transaction_inlineformset.is_valid():
            po_obj = po_form.save(commit=False)
            po_obj.created_by = request.user
            po_obj.company = request.user.company
            po_obj.purchase_code = po_code
            if 'Save as draft' in request.POST:
                po_obj.status = "drafted"
            po_obj.tax = tax_percentage
            po_obj.save()
            print(po_obj.subtotal_price_after_discount)
            po_transaction_inlineformset = purchase_transaction_formset(request.POST, instance=po_obj,
                                                                        form_kwargs={'user': request.user})
            if po_transaction_inlineformset.is_valid():
                for form in po_transaction_inlineformset:
                    po_transaction_obj = form.save(commit=False)
                    po_transaction_obj.created_by = request.user
                    po_transaction_obj.balance = po_transaction_obj.quantity
                    if po_obj.discount_type == "percentage":
                        po_transaction_obj.discount_percentage = po_obj.discount
                    elif po_obj.discount_type == "amount":
                        # TODO: implement this
                        po_transaction_obj.discount_percentage = po_obj.discount
                    po_transaction_obj.save()
                messages.success(request, 'Saved Successfully')
                if 'Save and exit' in request.POST:
                    return redirect('orders:list-po')

            else:
                messages.error(request,po_transaction_inlineformset.errors)
                print(po_transaction_inlineformset.errors)
        else:
            # messages.add_message(request, messages.error, po_form.errors)
            # messages.add_message(request, messages.error, po_transaction_inlineformset.errors)
            print(po_form.errors)
            print(po_transaction_inlineformset.errors)
    context = {
        'po_form': po_form,
        'po_transaction_inlineformset': po_transaction_inlineformset,
        'title': 'New Purchase Order',
        'tax' : tax_percentage
    }

    return render(request, 'create-purchase-order.html', context=context)


def list_purchase_order_view(request):
    """
    List all purchase orders in the user company :model:`Order.PurchaseOrder`.

    **Context**

    ``purchase_orders_list``
        A list of purchase orders in user's company :model:`Order.PurchaseOrder`.
     ``title``
        A string representing the title of the rendered HTML page


    **Template:**

    :template:`orders/templates/list-purchase_orders.html`

    """
    purchase_orders = PurchaseOder.objects.filter(company=request.user.company)
    context = {
        'purchase_orders_list': purchase_orders,
        'title': "Purchase Orders",
    }
    return render(request, 'list-purchase_orders.html', context=context)


def update_purchase_order_view(request, id):
    """
    Update a purchase order only if its status is "drafted" :model:`Orders.PurchaseOrder`.

    **Context**

      ``po_form``
          An instance of :form:`Orders.forms.PurchaseOrderCreationForm`.
      ``po_transaction_inlineformset``
          An instance of :inlineformset_factory:`Orders.forms.purchase_transaction_formset`
      ``title``
          A string representing the title of the rendered HTML page
      ``update``
         A boolean value set to True in case of updating purchase order


    **Template:**

      :template:`orders/templates/create-purchase-order.html`

    """
    order = PurchaseOder.objects.get(pk=id)
    purchase_order_form = PurchaseOrderCreationForm(instance=order, user=request.user)
    po_transaction_inlineformset = purchase_transaction_formset(instance=order, form_kwargs={'user': request.user})
    purchase_order_form.fields["my_total_price_after_discount"].initial = order.global_price_after_discount
    for form in po_transaction_inlineformset:
        form.fields["after_discount"].initial = form.instance.total_price_after_discount

    if request.method == 'POST':
        purchase_order_form = PurchaseOrderCreationForm(request.POST, instance=order, user=request.user)
        po_transaction_inlineformset = purchase_transaction_formset(request.POST, instance=order,
                                                                    form_kwargs={'user': request.user})
        if purchase_order_form.is_valid() and po_transaction_inlineformset.is_valid():
            po_obj = purchase_order_form.save(commit=False)
            po_obj.last_updated_by = request.user
            if 'Save as open' in request.POST:
                po_obj.status = 'open' # otherwise status will be as it was:"drafted"
            po_obj.save()
            po_transaction_inlineformset = purchase_transaction_formset(request.POST, instance=po_obj,
                                                                        form_kwargs={'user': request.user})
            if po_transaction_inlineformset.is_valid():
                for form in po_transaction_inlineformset:
                    po_transaction_obj = form.save(commit=False)
                    po_transaction_obj.last_updated_by = request.user
                    #po_transaction_obj.balance = po_transaction_obj.quantity
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
                messages.error(request,po_transaction_inlineformset.errors)
                print(po_transaction_inlineformset.errors)
        else:
            messages.add_message(request, messages.error, purchase_order_form.errors)
            messages.add_message(request, messages.error, po_transaction_inlineformset.errors)
            print(purchase_order_form.errors)
            print(po_transaction_inlineformset.errors)

    context = {
        'po_form': purchase_order_form,
        'po_transaction_inlineformset': po_transaction_inlineformset,
        'title': 'Update Purchase Order',
        'update': True,

    }
    return render(request, 'create-purchase-order.html', context)


def delete_purchase_order_view(request, id):
    """
        Delete a purchase order :model:`Order.PurchaseOrder`.

    """
    po_order = PurchaseOder.objects.get(pk=id)
    deleted = po_order.delete()
    if deleted:
        return redirect('orders:list-po')
    else:
        messages.error(request, 'Record could not be deleted')
        print("item not deleted")


def create_sales_order_view(request):
    so_form = SaleOrderCreationForm(user=request.user)
    so_transaction_inlineformset = sale_transaction_formset(form_kwargs={'user': request.user})
    rows_number = SalesOrder.objects.all().count()
    so_code = "SO-" + str(date.today()) + "-" + get_seq(rows_number)
    so_form.fields['sale_code'].initial = so_code
    if request.method == 'POST':
        so_form = SaleOrderCreationForm(request.POST, user=request.user)
        so_transaction_inlineformset = sale_transaction_formset(request.POST, form_kwargs={'user': request.user})
        if so_form.is_valid() and so_transaction_inlineformset.is_valid():
            so_obj = so_form.save(commit=False)
            so_obj.created_by = request.user
            so_obj.company = request.user.company
            so_obj.sale_code = so_code
            try:
                tax = Tax.objects.get(name='VAT')
                tax_percentage = tax.value / 100
            except ObjectDoesNotExist:
                print(ObjectDoesNotExist)
                tax_percentage = Decimal(0.14)
            so_obj.tax = tax_percentage
            so_obj.save()
            so_transaction_inlineformset = sale_transaction_formset(request.POST, instance=so_obj,
                                                                    form_kwargs={'user': request.user})
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
        'title': 'New Sale Order',

    }
    return render(request, 'create-sale-order.html', context=subcontext)


def list_sale_order_view(request):
    sale_orders = SalesOrder.objects.filter(company=request.user.company)
    subcontext = {
        'sale_orders_list': sale_orders
    }
    return render(request, 'list-sale_orders.html', context=subcontext)


def update_sale_order_view(request, id):
    order = SalesOrder.objects.get(pk=id)
    sale_order_form = SaleOrderCreationForm(instance=order, user=request.user)
    so_transaction_inlineformset = sale_transaction_formset(instance=order, form_kwargs={'user': request.user})
    for form in so_transaction_inlineformset:
        print(form.instance.item.id)
        item = form.instance.item
        uom = item.uom

        unit_price = item.avg_cost.amount
        print(unit_price)
        form.fields["temp_uom"].initial = uom
        form.fields["price_per_unit"].initial = unit_price
    if request.method == 'POST':
        sale_order_form = SaleOrderCreationForm(request.POST, instance=order, user=request.user)
        so_transaction_inlineformset = sale_transaction_formset(request.POST, instance=order,
                                                                form_kwargs={'user': request.user})
        if sale_order_form.is_valid() and so_transaction_inlineformset.is_valid():
            so_obj = sale_order_form.save(commit=False)
            so_obj.last_updated_by = request.user
            so_obj.save()
            so_transaction_inlineformset = sale_transaction_formset(request.POST, instance=so_obj,
                                                                    form_kwargs={'user': request.user})
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


def get_item(request, id):
    item = Item.objects.select_related().get(pk=id)
    serialized = ItemSerializer(item)
    return JSONResponse(serialized.data, content_type='application/json')


class ItemAutocomplete(autocomplete.Select2QuerySetView):
    """
    This class is used to search for items in a dropdown list
    """
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Item.objects.none()  
        qs = Item.objects.filter(company=self.request.user.company)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class SoItemAutocomplete(autocomplete.Select2QuerySetView):
    print("inside ItemAutocomplete")

    def get_queryset(self):
        print("inside get_queryset ItemAutocomplete")
        if not self.request.user.is_authenticated:
            return Inventory_Balance.objects.none()
        inventory_items = Inventory_Balance.objects.filter(company=self.request.user.company).values('item').distinct()
        myids = [record['item'] for record in inventory_items]
        qs = Item.objects.filter(id__in=myids)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


def list_purchases_for_receiving(request):
    """
    List all purchase orders in the user company that are not drafted :model:`Order.PurchaseOrder`.

    **Context**

    ``purchase_orders_list``
        A list of purchase orders in user's company :model:`Order.PurchaseOrder`.

    ``receiving``
        A boolean that takes 'True' value in case purchase orders are listed in receivings page.

     ``title``
        A string representing the title of the rendered HTML page.


    **Template:**

    :template:`orders/templates/list-purchase_orders.html`

    """
    purchase_orders = PurchaseOder.objects.filter(~Q(status='drafted')).order_by('-status')
    context = {
        'purchase_orders_list': purchase_orders,
        'receiving': True,
        'title': "Purchase Orders Transactions",

    }
    return render(request, 'list-purchase_orders.html', context=context)


def list_receiving(request, id, return_to):
    receivings = MaterialTransaction1.objects.filter(purchase_order__id=id)
    po = PurchaseOder.objects.get(id=id)
    status = po.status
    subcontext = {
        'pk': id,
        'receivings': receivings,
        'status': status,
        'return_to': return_to,

    }
    return render(request, 'list-receiving.html', context=subcontext)


def create_receiving(request, id):
    material_form = MaterialTransactionCreationForm()
    material_lines_formset = MaterialTransactionCreation_formset(form_kwargs={'id': id, 'user': request.user})
    purchase_lines = PurchaseTransaction.objects.filter(purchase_order__id=id)
    purchase_order = PurchaseOder.objects.get(id=id)
    rows_number = MaterialTransaction1.objects.all().count()
    transaction_code = "REC-" + str(date.today()) + "-" + get_seq(rows_number)
    material_form.fields["transaction_code"].initial = transaction_code

    if request.method == 'POST':
        material_form = MaterialTransactionCreationForm(request.POST)
        if material_form.is_valid():
            material_obj = material_form.save(commit=False)
            material_obj.company = request.user.company
            material_obj.purchase_order = purchase_order
            material_obj.transaction_code = transaction_code
            material_obj.created_by = request.user
            material_obj.save()
            material_lines_formset = MaterialTransactionCreation_formset(request.POST, instance=material_obj,
                                                                         form_kwargs={'id': id, 'user': request.user})
        if material_lines_formset.is_valid():
            receiving_objs = material_lines_formset.save(commit=False)
            for obj in receiving_objs:
                obj.created_by = request.user
                obj.transaction_type = 'inbound'
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
                return redirect('orders:list-receiving', id=id, return_to='list')
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


def view_purchase_order(request, id, flag, return_to):
    # flag parameter is used to determine if the request if from purchase order screen or transactions screen
    purchase_order = PurchaseOder.objects.get(id=id)
    purchase_lines = PurchaseTransaction.objects.filter(purchase_order__id=id)
    print("HERE IS MY FLag", flag)
    subcontext = {
        'po': purchase_order,
        'po_lines': purchase_lines,
        'flag': flag,
        'return_to': return_to,

    }
    return render(request, 'view-po.html', context=subcontext)


def view_sale_order(request, id):
    sale_order = SalesOrder.objects.get(id=id)
    sale_lines = SalesTransaction.objects.filter(sales_order__id=id)
    tax_value = sale_order.tax * 100
    subcontext = {
        'so': sale_order,
        'so_lines': sale_lines,
        'tax': tax_value,

    }
    return render(request, 'view-so.html', context=subcontext)


def list_all_transactions(request):
    transaction_lines = MaterialTransactionLines.objects.filter(material_transaction__company=request.user.company)

    context = {
        'transactions': transaction_lines,
    }
    return render(request, 'list-transactions.html', context=context)


def view_transaction_lines(request, id):
    transaction_lines = MaterialTransactionLines.objects.filter(material_transaction=id)
    transaction = MaterialTransaction1.objects.get(id=id)
    context = {
        'transactions_line': transaction_lines,
        'transaction': transaction,
    }
    return render(request, 'list-transactions-lines.html', context=context)


def create_tax(request):
    tax_form = TaxForm()
    if request.method == 'POST':
        tax_form = TaxForm(request.POST)
        if tax_form.is_valid():
            tax_obj = tax_form.save(commit=False)
            tax_obj.company = request.user.company
            tax_obj.created_by = request.user
            tax_obj.save()
            if 'Save and exit' in request.POST:
                return redirect('orders:list-taxes')
            elif 'Save and add' in request.POST:
                return redirect('orders:create-tax')

    Context = {
        'tax_form': tax_form,
        'title': 'New Tax'

    }
    return render(request, 'create-tax.html', context=Context)


def list_taxes(request):
    taxes = Tax.objects.all()
    context = {
        'tax_list': taxes,
        'title': "Taxes",
    }
    return render(request, 'list-taxes.html', context=context)


def update_tax(request, id):
    tax = Tax.objects.get(id=id)
    tax_form = TaxForm(instance=tax)
    if request.method == 'POST':
        tax_form = TaxForm(request.POST, instance=tax)
        if tax_form.is_valid():
            tax_obj = tax_form.save(commit=False)
            tax_obj.last_updated_by = request.user
            tax_obj.save()
            if 'Save and exit' in request.POST:
                return redirect('orders:list-taxes')

    Context = {
        'tax_form': tax_form,
        'title': 'Update Tax',
        'update': True,

    }
    return render(request, 'create-tax.html', context=Context)


def delete_tax_view(request, id):
    required_tax = Tax.objects.get(id=id)
    try:
        required_tax.delete()
    except ProtectedError:
        error_message = "This object can't be deleted!!"
        messages.error(request, error_message)
    return redirect('orders:list-taxes')


def load_uoms(request):
    item_id = request.GET.get('item')
    item = Item.objects.get(id=item_id)
    uoms = Uom.objects.filter(category=item.uom.category)
    return render(request, 'load-uoms.html', {'uoms': uoms, 'default': item.uom})
