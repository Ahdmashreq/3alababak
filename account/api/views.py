from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from account.models import Customer, Supplier
from .serializers import CustomerSerializer, SupplierSerializer


@api_view(['GET', ])
def api_list_customers(request):
    customers = Customer.objects.filter(company=request.user.company).order_by("last_updated_at")
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
def api_list_suppliers(request):
    suppliers = Supplier.objects.all().order_by("last_updated_at")
    serializer = SupplierSerializer(suppliers, many=True)
    return Response(serializer.data)
