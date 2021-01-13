from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages

from account.forms import (CustomerCreationForm, SupplierCreationForm, customer_address_formset,
                           supplier_address_formset, CompanyCreationForm, )
from account.models import Customer, Supplier


def create_customer_address_account(request):
    """
    Create a customer account with address :model:`Account.Customer,Account.Address`.

    **Context**

    ``account_form``
        An instance of :form:`Account.forms.CustomerCreationForm`.
    ``address_inlineformset``
        An instance of :inlineformset_factory:`Account.forms.customer_address_formset`
    ``title``
        A string representing the title of the rendered HTML page
    ``account_type``
        A string that takes either `Customer` or `Supplier`

    **Template:**

    :template:`account/templates/create-account.html`

    """
    customer_form = CustomerCreationForm()
    address_inlineformset = customer_address_formset()
    if request.method == 'POST':
        customer_form = CustomerCreationForm(request.POST)
        address_inlineformset = customer_address_formset(request.POST)
        if customer_form.is_valid() and address_inlineformset.is_valid():
            customer_obj = customer_form.save(commit=False)
            customer_obj.created_by = request.user
            customer_obj.company = request.user.company
            flag = False
            try:
                flag = True
                customer_obj.save()
            except IntegrityError:
                # Slug field value is duplicated
                messages.error(request, "Customer first name and last name already exist")
            if flag:
                # save address only if customer account is saved
                address_inlineformset = customer_address_formset(request.POST, instance=customer_obj)
                if address_inlineformset.is_valid():
                    address_obj = address_inlineformset.save(commit=False)
                    for address in address_obj:
                        address.created_by = request.user
                        address.save()
                    # Success only after saving both customer instance and addresses
                    messages.success(request, 'Saved Successfully')
                    if 'Save and exit' in request.POST:
                        return redirect('account:list-customers')
                    elif 'Save and add' in request.POST:
                        return redirect('account:create-customer')
                else:
                    messages.error(request, address_inlineformset.errors)
                    print(address_inlineformset.errors)
        else:
            messages.add_message(request, messages.error, customer_form.errors)
            messages.add_message(request, messages.error, address_inlineformset.errors)
            print("Customer form errors are {}".format(customer_form.errors))
            print("Address forms error are {}".format(address_inlineformset.errors))

    customer_information_context = {
        'account_form': customer_form,
        'address_inlineformset': address_inlineformset,
        'title': 'New Customer',
        'account_type': 'Customer'  # this key value is used to differentiate between account types in template
    }
    return render(request, 'create-account.html', context=customer_information_context)


def create_supplier_address_account(request):
    """
    Create a supplier account :model:`Account.Supplier,Account.Address`.

    **Context**

    ``account_form``
        An instance of :form:`Account.forms.SupplierCreationForm`.
    ``address_inlineformset``
        An instance of :inlineformset_factory:`Account.forms.supplier_address_formset`
    ``title``
        A string representing the title of the rendered HTML page


    **Template:**

    :template:`account/templates/create-account.html`

    """
    supplier_form = SupplierCreationForm()
    address_inlineformset = supplier_address_formset()
    if request.method == 'POST':
        supplier_form = SupplierCreationForm(request.POST)
        address_inlineformset = supplier_address_formset(request.POST)
        if supplier_form.is_valid() and address_inlineformset.is_valid():
            supplier_obj = supplier_form.save(commit=False)
            supplier_obj.created_by = request.user
            supplier_obj.company = request.user.company
            flag = False
            try:
                flag = True
                supplier_obj.save()
            except IntegrityError:
                # Slug field value is duplicated
                messages.error(request, "Supplier first name and last name already exist")
            if flag:
                # save address only if supplier account is saved
                address_inlineformset = supplier_address_formset(request.POST, instance=supplier_obj)
                if address_inlineformset.is_valid():
                    address_obj = address_inlineformset.save(commit=False)
                    for address in address_obj:
                        address.created_by = request.user
                        address.save()
                    # Success only after saving both supplier instance and addresses
                    messages.success(request, 'Saved Successfully')
                    if 'Save and exit' in request.POST:
                        return redirect('account:list-suppliers')
                    elif 'Save and add' in request.POST:
                        return redirect('account:create-supplier')
                else:
                    messages.error(request, address_inlineformset.errors)
                    print(address_inlineformset.errors)
        else:
            messages.add_message(request, messages.error, supplier_form.errors)
            messages.add_message(request, messages.error, address_inlineformset.errors)
            print("Supplier form errors are {}".format(supplier_form.errors))
            print("Address forms error are {}".format(address_inlineformset.errors))

    supplier_information_context = {
        'account_form': supplier_form,
        'address_inlineformset': address_inlineformset,
        'title': 'New Supplier'

    }
    return render(request, 'create-account.html', context=supplier_information_context)


def create_company(request):
    form = CompanyCreationForm()
    if request.method == 'POST':
        form = CompanyCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home:homepage')
    req_form = {'company_form': form}
    return render(request, 'create-company.html', context=req_form)


def list_suppliers_view(request):
    """
      List all suppliers in the user company :model:`Account.Supplier`.

      **Context**

      ``suppliers_list``
          A list of suppliers in user's company :model:`Account.Supplier`.


      **Template:**

      :template:`account/templates/list-suppliers.html`

      """
    suppliers_list = Supplier.objects.filter(company=request.user.company)
    context = {
        'suppliers_list': suppliers_list,
    }
    return render(request, 'list-suppliers.html', context)


def list_customer_view(request):
    """
    List all customers in the user company :model:`Account.Customer`.

    **Context**

    ``customers_list``
        A list of customer in user's company :model:`Account.Customer`.


    **Template:**

    :template:`account/templates/list-customers.html`

    """
    customers_list = Customer.objects.filter(company=request.user.company)
    context = {
        'customers_list': customers_list,
    }
    return render(request, 'list-customers.html', context)


def update_customer_view(request, slug):
    """
       Update a customer account :model:`Account.Customer,Account.Address`.

       **Context**

       ``account_form``
           An instance of :form:`Account.forms.CustomerCreationForm`.
       ``address_inlineformset``
           An instance of :inlineformset_factory:`Account.forms.customer_address_formset`
       ``title``
           A string representing the title of the rendered HTML page
       ``account_type``
           A string that takes either `Customer` or `Supplier`
       ``update``
         A boolean value set to True in case of updating account

       **Template:**

       :template:`account/templates/create-account.html`

       """
    customer = Customer.objects.get(slug=slug)
    customer_form = CustomerCreationForm(instance=customer)
    address_inlineformset = customer_address_formset(instance=customer)
    if request.method == 'POST':
        customer_form = CustomerCreationForm(request.POST, instance=customer)
        address_inlineformset = customer_address_formset(request.POST, instance=customer)
        if customer_form.is_valid() and address_inlineformset.is_valid():
            customer_obj = customer_form.save(commit=False)
            customer_obj.last_updated_by = request.user
            flag = False
            try:
                customer_obj.save()
                flag = True
            except IntegrityError:
                # Slug field value is duplicated
                messages.error(request, "Customer first name and last name already exist")
            if flag:
                address_inlineformset = customer_address_formset(request.POST, instance=customer_obj)
                if address_inlineformset.is_valid():
                    address_obj = address_inlineformset.save(commit=False)
                    for address in address_obj:
                        address.last_updated_by = request.user
                        address.save()
                    messages.success(request, 'Saved Successfully')
                    if 'Save and exit' in request.POST:
                        return redirect('account:list-customers')

                else:
                    messages.error(request, address_inlineformset.errors)
                    print(address_inlineformset.errors)
        else:
            messages.error(request, customer_form.errors)
            print(address_inlineformset.errors)
            print(customer_form.errors)

    context = {
        'account_form': customer_form,
        'address_inlineformset': address_inlineformset,
        'title': 'Update Customer',
        'account_type': 'Customer',
        'update': True,

    }
    return render(request, 'create-account.html', context)


def update_supplier_view(request, slug):
    """
     Update a supplier account :model:`Account.Supplier,Account.Address`.

     **Context**

     ``account_form``
         An instance of :form:`Account.forms.SupplierCreationForm`.
     ``address_inlineformset``
         An instance of :inlineformset_factory:`Account.forms.supplier_address_formset`
     ``title``
         A string representing the title of the rendered HTML page
     ``update``
         A boolean value set to True in case of updating account

     **Template:**

     :template:`account/templates/create-account.html`

     """
    supplier = Supplier.objects.get(slug=slug)
    supplier_form = SupplierCreationForm(instance=supplier)
    address_inlineformset = supplier_address_formset(instance=supplier)
    if request.method == 'POST':
        supplier_form = SupplierCreationForm(request.POST, instance=supplier)
        address_inlineformset = supplier_address_formset(request.POST, instance=supplier)
        if supplier_form.is_valid() and address_inlineformset.is_valid():
            supplier_obj = supplier_form.save(commit=False)
            supplier_obj.last_updated_by = request.user
            flag = False
            try:
                supplier_obj.save()
                flag = True
            except IntegrityError:
                # Slug field value is duplicated
                messages.error(request, "Supplier first name and last name already exist")
            if flag:
                address_inlineformset = supplier_address_formset(request.POST, instance=supplier_obj)
                if address_inlineformset.is_valid():
                    address_obj = address_inlineformset.save(commit=False)
                    for address in address_obj:
                        address.last_updated_by = request.user
                        address.save()
                    messages.success(request, 'Saved Successfully')
                    if 'Save and exit' in request.POST:
                        return redirect('account:list-suppliers')

                else:
                    messages.error(request, address_inlineformset.errors)
                    print(address_inlineformset.errors)
        else:
            messages.add_message(request, messages.error, supplier_form.errors)
            messages.add_message(request, messages.error, address_inlineformset.errors)
            print("Supplier form errors are {}".format(supplier_form.errors))
            print("Address forms error are {}".format(address_inlineformset.errors))

    context = {
        'account_form': supplier_form,
        'address_inlineformset': address_inlineformset,
        'title': 'Update Supplier',
        'update': True

    }
    return render(request, 'create-account.html', context)


def delete_customer(request, id):
    """
       Delete a customer account :model:`Account.Customer`.

    """
    customer = Customer.objects.get(pk=id)
    deleted = customer.delete()
    if deleted:
        messages.success(request, 'Deleted Successfully')
        return redirect('account:list-customers')
    else:
        messages.error(request, 'Record could not be deleted')
        print("item not deleted")


def delete_supplier(request, id):
    """
     Delete a supplier account :model:`Account.Supplier`.

    """
    supplier = Supplier.objects.get(pk=id)
    deleted = supplier.delete()
    if deleted:
        messages.success(request, 'Deleted Successfully')
        return redirect('account:list-suppliers')
    else:
        messages.error(request, 'Record could not be deleted')
        print("item not deleted")
