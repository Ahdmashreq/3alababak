from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from account.models import Customer, Supplier
from .serializers import CustomerSerializer, SupplierSerializer, AddressSerializer
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_list_customers(request):
    customers = Customer.objects.filter(company=request.user.company).order_by("last_updated_at")
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)


class CustomerListView(ListAPIView):
    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('status', 'first_name', 'email',)
    ordering_fields = ('first_name', 'status',)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        company = self.request.user.company
        return Customer.objects.filter(company=company)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_list_suppliers(request):
    suppliers = Supplier.objects.filter(company=request.user.company).order_by("last_updated_at")
    serializer = SupplierSerializer(suppliers, many=True)
    return Response(serializer.data)


class SupplierListView(ListAPIView):
    serializer_class = SupplierSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('status', 'first_name', 'email',)
    ordering_fields = ('first_name', 'status',)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        company = self.request.user.company
        return Supplier.objects.filter(company=company)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_add_customer(request):
    customer_serializer = CustomerSerializer(data=request.data, context={'request': request})
    if customer_serializer.is_valid():
        customer_serializer.save(company=request.user.company, created_by=request.user)
        return Response(customer_serializer.data, status=status.HTTP_201_CREATED)
    return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', ])
@permission_classes((IsAuthenticated,))
def api_update_customer(request, slug):
    data = {}
    try:
        customer = Customer.objects.get(slug=slug)
    except Customer.DoesNotExist:
        data['failure'] = 'record not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if customer.company != request.user.company:
        data['failure'] = 'you are not allowed to edit this customer'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'PUT':
        partial = False
    elif request.method == 'PATCH':
        partial = True
    customer_serializer = CustomerSerializer(customer, data=request.data, context={'request': request}, partial=partial)
    if customer_serializer.is_valid():
        customer_serializer.save()
        # TODO : find a standardized way to send the response
        data["success"] = 'update successful'
        return Response(customer_serializer.data, status=status.HTTP_200_OK)
    return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_customer(request, slug):
    data = {}
    try:
        customer = Customer.objects.get(slug=slug)
    except Customer.DoesNotExist:
        data['failure'] = 'record not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if customer.company != request.user.company:
        data['failure'] = 'you are not allowed to delete this customer'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    operation = customer.delete()
    if operation:
        data['success'] = 'delete successful'
        st = status.HTTP_200_OK
    else:
        data['failure'] = 'delete failed'
        st = status.HTTP_400_BAD_REQUEST
    return Response(data=data, status=st)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_view_customer(request, slug):
    data = {}
    try:
        customer = Customer.objects.get(slug=slug)
    except Customer.DoesNotExist:
        data['failure'] = 'record not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if customer.company != request.user.company:
        data['failure'] = 'you are not allowed to view this customer'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    serializer = CustomerSerializer(customer, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_add_supplier(request):
    supplier_serializer = SupplierSerializer(data=request.data, context={'request': request})
    if supplier_serializer.is_valid():
        supplier_serializer.save(company=request.user.company, created_by=request.user)
        return Response(supplier_serializer.data, status=status.HTTP_201_CREATED)
    return Response(supplier_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', ])
@permission_classes((IsAuthenticated,))
def api_update_supplier(request, slug):
    data = {}
    try:
        supplier = Supplier.objects.get(slug=slug)
    except Supplier.DoesNotExist:
        data['failure'] = 'record not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if supplier.company != request.user.company:
        data['failure'] = 'you are not allowed to edit this supplier'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'PUT':
        partial = False
    elif request.method == 'PATCH':
        partial = True
    supplier_serializer = SupplierSerializer(supplier, data=request.data, context={'request': request}, partial=partial)
    if supplier_serializer.is_valid():
        supplier_serializer.save()
        # TODO : find a standardized way to send the response
        data["success"] = 'update successful'
        return Response(supplier_serializer.data, status=status.HTTP_200_OK)
    return Response(supplier_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_supplier(request, slug):
    data = {}
    try:
        supplier = Supplier.objects.get(slug=slug)
    except Supplier.DoesNotExist:
        data['failure'] = 'record not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if supplier.company != request.user.company:
        data['failure'] = 'you are not allowed to delete this supplier'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    operation = supplier.delete()
    if operation:
        data['success'] = 'delete successful'
        st = status.HTTP_200_OK
    else:
        data['failure'] = 'delete failed'
        st = status.HTTP_400_BAD_REQUEST
    return Response(data=data, status=st)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_view_supplier(request, slug):
    data = {}
    try:
        supplier = Supplier.objects.get(slug=slug)
    except Supplier.DoesNotExist:
        data['failure'] = 'record not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if supplier.company != request.user.company:
        data['failure'] = 'you are not allowed to view this supplier'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    serializer = SupplierSerializer(supplier, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)
