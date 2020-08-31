from django.shortcuts import render, redirect
from account.forms import (CustomerCreationForm, SupplierCreationForm, customer_address_formset,
                           supplier_address_formset, CompanyCreationForm, )
from account.models import Customer, Supplier
from django.contrib import messages


def create_customer_address_account(request):
    if request.method == 'POST':
        customer_form = CustomerCreationForm(request.POST)
        address_inlineformset = customer_address_formset(request.POST)
        if customer_form.is_valid() and address_inlineformset.is_valid():
            customer_obj = customer_form.save(commit=False)
            customer_obj.created_by = request.user
            customer_obj.company = request.user.company
            customer_obj.save()
            address_inlineformset = customer_address_formset(request.POST, instance=customer_obj)
            if address_inlineformset.is_valid():
                address_obj = address_inlineformset.save(commit=False)
                for address in address_obj:
                    address.created_by = request.user
                    address.save()

                messages.success(request, 'Saved Successfully')
                print("***************")
                if 'Save and exit' in request.POST:
                    return redirect('account:list-customers')
                elif 'Save and add' in request.POST:
                    return redirect('account:create-customer')
            else:
                print(address_inlineformset.errors)
        else:
            print(customer_form.errors)
    else:
        customer_form = CustomerCreationForm()
        address_inlineformset = customer_address_formset()

    customer_information_context = {
        'account_form': customer_form,
        'address_inlineformset': address_inlineformset,
        'title': 'New Customer',
        'account_type':'Customer'
    }
    return render(request, 'create-supplier.html', context=customer_information_context)


def create_supplier_address_account(request):
    if request.method == 'POST':
        supplier_form = SupplierCreationForm(request.POST)
        address_inlineformset = supplier_address_formset(request.POST)
        if supplier_form.is_valid() and address_inlineformset.is_valid():
            supplier_obj = supplier_form.save(commit=False)
            supplier_obj.created_by = request.user
            supplier_obj.company = request.user.company
            supplier_obj.save()
            address_inlineformset = supplier_address_formset(request.POST, instance=supplier_obj)
            if address_inlineformset.is_valid():
                address_obj = address_inlineformset.save(commit=False)
                for address in address_obj:
                    address.created_by = request.user
                    address.save()

                messages.success(request, 'Saved Successfully')
                if 'Save and exit' in request.POST:
                    return redirect('account:list-suppliers')
                elif 'Save and add' in request.POST:
                    return redirect('account:create-supplier')
            else:
                print(address_inlineformset.errors)
        else:
            print(supplier_form.errors)
    else:
        supplier_form = SupplierCreationForm()
        address_inlineformset = supplier_address_formset()

    supplier_information_context = {
        'account_form': supplier_form,
        'address_inlineformset': address_inlineformset,
        'title': 'New Supplier'

    }

    return render(request, 'create-supplier.html', context=supplier_information_context)


def create_company(request):
    form = CompanyCreationForm()
    if request.method == 'POST':
        form = CompanyCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home:homepage')
    req_form = {'company_form': form}
    return render(request, 'create-company.html', context=req_form)


def list_customers(request):
    customers = Customer.objects.all().values()
    supcontext = {'dict_customers': customers}
    return render(request, 'list_customers.html', context=supcontext)


def list_suppliers(request):
    suppliers = Supplier.objects.all().values()
    supcontext = {'dict_suppliers': suppliers}
    return render(request, 'list_suppliers.html', context=supcontext)


def list_suppliers_view(request):
    supliers_list = Supplier.objects.all()
    supContext = {
        'supliers_list': supliers_list,
    }
    return render(request, 'list-suppliers.html', supContext)


def list_customer_view(request):
    customers_list = Customer.objects.all()
    supContext = {
        'customers_list': customers_list,
    }
    return render(request, 'list-customers.html', supContext)


def update_customer_view(request, id):
    customer = Customer.objects.get(pk=id)
    customer_form = CustomerCreationForm(instance=customer)
    address_inlineformset = customer_address_formset(instance=customer)
    if request.method == 'POST':
        customer_form = CustomerCreationForm(request.POST, instance=customer)
        address_inlineformset = customer_address_formset(request.POST, instance=customer)
        if customer_form.is_valid() and address_inlineformset.is_valid():
            customer_obj = customer_form.save(commit=False)
            customer_obj.last_updated_by = request.user
            customer_obj.save()
            address_inlineformset = customer_address_formset(request.POST, instance=customer_obj)
            if address_inlineformset.is_valid():
                address_obj = address_inlineformset.save(commit=False)
                for address in address_obj:
                    address.last_updated_by = request.user
                    address.save()
                messages.success(request, 'Saved Successfully')
                return redirect('account:list-customers')
            else:
                print(address_inlineformset.errors)
        else:
            print(customer_form.errors)

    supContext = {
        'account_form': customer_form,
        'address_inlineformset': address_inlineformset,
        'title': 'Update Customer'

    }
    return render(request, 'create-supplier.html', supContext)


def update_supplier_view(request, id):
    supplier = Supplier.objects.get(pk=id)
    supplier_form = SupplierCreationForm(instance=supplier)
    address_inlineformset = supplier_address_formset(instance=supplier)
    if request.method == 'POST':
        supplier_form = SupplierCreationForm(request.POST, instance=supplier)
        address_inlineformset = supplier_address_formset(request.POST, instance=supplier)
        if supplier_form.is_valid() and address_inlineformset.is_valid():
            supplier_obj = supplier_form.save(commit=False)
            supplier_obj.last_updated_by = request.user
            supplier_obj.save()
            address_inlineformset = supplier_address_formset(request.POST, instance=supplier_obj)
            if address_inlineformset.is_valid():
                address_obj = address_inlineformset.save(commit=False)
                for address in address_obj:
                    address.last_updated_by = request.user
                    address.save()
                messages.success(request, 'Saved Successfully')
                return redirect('account:list-suppliers')

            else:
                print(address_inlineformset.errors)
        else:
            print(supplier_form.errors)

    supContext = {
        'account_form': supplier_form,
        'address_inlineformset': address_inlineformset,
        'title': 'Update Supplier'

    }
    return render(request, 'create-supplier.html', supContext)


def delete_customer(request, id):
    customer = Customer.objects.get(pk=id)
    deleted = customer.delete()
    if deleted:
        return redirect('account:list-customers')
    else:
        print("item not deleted")


def delete_supplier(request, id):
    supplier = Supplier.objects.get(pk=id)
    deleted = supplier.delete()
    if deleted:
        return redirect('account:list-suppliers')
    else:
        print("item not deleted")
