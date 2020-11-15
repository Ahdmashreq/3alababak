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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            data = {"success": True, "count": paginated_response.data["count"], "data": serializer.data, }
            return Response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = {"success": True, "data": serializer.data}
        return Response(data)


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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            data = {"success": True, "count": paginated_response.data["count"], "data": serializer.data, }
            return Response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = {"success": True, "data": serializer.data}
        return Response(data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_add_customer(request):
    customer_serializer = CustomerSerializer(data=request.data, context={'request': request})
    if customer_serializer.is_valid():
        try:
            customer_serializer.save(company=request.user.company, created_by=request.user)
        except IntegrityError:
            data = {"success": False, "error": {"code": 400, "message": "Customer name exits"}}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        data = {"success": True, "data": customer_serializer.data}
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = {"success": False, "error": {"code": 400, "message": customer_serializer.errors}}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', ])
@permission_classes((IsAuthenticated,))
def api_update_customer(request, slug):
    try:
        customer = Customer.objects.filter(company=request.user.company).get(slug=slug)
    except Customer.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        partial = False
    elif request.method == 'PATCH':
        partial = True
    customer_serializer = CustomerSerializer(customer, data=request.data, context={'request': request}, partial=partial)
    if customer_serializer.is_valid():
        try:
            customer_serializer.save()
        except IntegrityError:
            data = {"success": False, "error": {"code": 400, "message": "Customer name exits"}}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        data = {"success": True, "data": customer_serializer.data}
        return Response(data, status=status.HTTP_200_OK)
    else:
        data = {"success": False, "error": {"code": 400, "message": customer_serializer.errors}}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_customer(request, slug):
    try:
        customer = Customer.objects.filter(company=request.user.company).get(slug=slug)
    except Customer.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    operation = customer.delete()
    if operation:
        data = {"success": True}
        return Response(data=data, status=status.HTTP_200_OK)
    else:
        data = {"success": False}
        return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_view_customer(request, slug):
    try:
        customer = Customer.objects.filter(company=request.user.company).get(slug=slug)
    except Customer.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomerSerializer(customer, many=False)
    data = {"success": True, "data": serializer.data}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_add_supplier(request):
    supplier_serializer = SupplierSerializer(data=request.data, context={'request': request})
    if supplier_serializer.is_valid():
        try:
            supplier_serializer.save(company=request.user.company, created_by=request.user)
        except IntegrityError:
            data = {"success": False, "error": {"code": 400, "message": "supplier name exits"}}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        data = {"success": True, "data": supplier_serializer.data}
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = {"success": False, "error": {"code": 400, "message": supplier_serializer.errors}}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', ])
@permission_classes((IsAuthenticated,))
def api_update_supplier(request, slug):
    try:
        supplier = Supplier.objects.filter(company=request.user.company).get(slug=slug)
    except Supplier.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        partial = False
    elif request.method == 'PATCH':
        partial = True
    supplier_serializer = SupplierSerializer(supplier, data=request.data, context={'request': request}, partial=partial)
    if supplier_serializer.is_valid():
        try:
            supplier_serializer.save()
        except IntegrityError:
            data = {"success": False, "error": {"code": 400, "message": "Supplier name exits"}}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        data = {"success": True, "data": supplier_serializer.data}
        return Response(data, status=status.HTTP_200_OK)
    else:
        data = {"success": False, "error": {"code": 400, "message": supplier_serializer.errors}}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_supplier(request, slug):
    try:
        supplier = Supplier.objects.filter(company=request.user.company).get(slug=slug)
    except Supplier.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    operation = supplier.delete()
    if operation:
        data = {"success": True}
        return Response(data=data, status=status.HTTP_200_OK)
    else:
        data = {"success": False}
        return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_view_supplier(request, slug):
    try:
        supplier = Supplier.objects.filter(company=request.user.company).get(slug=slug)
    except Supplier.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    serializer = SupplierSerializer(supplier, many=False)
    data = {"success": True, "data": serializer.data}
    return Response(data, status=status.HTTP_200_OK)
