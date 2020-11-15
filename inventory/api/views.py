from django.db import IntegrityError
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from account.models import Customer, Supplier
from inventory.api.serializers import UomCategorySerializer, UomSerializer, CategorySerializer, BrandSerializer, \
    AttributeSerializer, StokeTakeSerializer, StokeEntrySerializer
from rest_framework.permissions import IsAuthenticated
import random

from inventory.models import UomCategory, Uom, Category, Brand, Attribute, StokeTake, StokeEntry, Product, Item
from inventory.views import create_stoke_transaction
from orders.models import Inventory_Balance


class UomCategoriesListView(ListAPIView):
    serializer_class = UomCategorySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_fields = ('id', 'slug',)
    ordering_fields = ('name',)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        company = self.request.user.company
        return UomCategory.objects.filter(company=company)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            data = {"success": True, "data": serializer.data, "count": paginated_response.data["count"]}
            return Response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = {"success": True, "data": serializer.data}
        return Response(data)


class UomListView(ListAPIView):
    serializer_class = UomSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_fields = ('category', 'id', 'slug',)
    ordering_fields = ('name', 'category',)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        company = self.request.user.company
        return Uom.objects.filter(company=company)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            data = {"success": True, "data": serializer.data, "count": paginated_response.data["count"]}
            return Response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = {"success": True, "data": serializer.data}
        return Response(data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_add_uom_category(request):
    uom_category_serializer = UomCategorySerializer(data=request.data)
    if uom_category_serializer.is_valid():
        try:
            uom_category_serializer.save(company=request.user.company, created_by=request.user)
            data = {"success": True, "data": uom_category_serializer.data}
            return Response(data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            data = {"success": False, "error": {"code": 400, "message": "Category already exists"}}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = {"success": False, "error": {"code": 400, "message": uom_category_serializer.errors}}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_add_uom(request):
    uom_serializer = UomSerializer(data=request.data)
    if uom_serializer.is_valid():
        try:
            uom_serializer.save(company=request.user.company, created_by=request.user)
            data = {"success": True, "data": uom_serializer.data}
            return Response(data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            data = {"success": False, "error": {"code": 400, "message": "Uom already exists in this category"}}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = {"success": False, "error": {"code": 400, "message": uom_serializer.errors}}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', ])
@permission_classes((IsAuthenticated,))
def api_update_uom_category(request, slug):
    try:
        uom_cateogry = UomCategory.objects.filter(company=request.user.company).get(slug=slug)
    except UomCategory.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        partial = False
    elif request.method == 'PATCH':
        partial = True
    uom_category_serializer = UomCategorySerializer(uom_cateogry, data=request.data, context={'request': request},
                                                    partial=partial)
    if uom_category_serializer.is_valid():
        try:
            uom_category_serializer.save(last_updated_by=request.user)
            data = {"success": True, "data": uom_category_serializer.data}
            return Response(data, status=status.HTTP_200_OK)
        except IntegrityError:
            data = {"success": False, "error": {"code": 400, "message": "Uom category already exists"}}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = {"success": False, "error": {"code": 400, "message": uom_category_serializer.errors}}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', ])
@permission_classes((IsAuthenticated,))
def api_update_uom(request, slug):
    try:
        uom = Uom.objects.filter(company=request.user.company).get(slug=slug)
    except Uom.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        partial = False
    elif request.method == 'PATCH':
        partial = True
    uom_category = UomSerializer(uom, data=request.data, context={'request': request},
                                 partial=partial)
    if uom_category.is_valid():
        try:
            uom_category.save(last_updated_by=request.user)
            data = {"success": True, "data": uom_category.data}
            return Response(data, status=status.HTTP_200_OK)
        except IntegrityError:
            data = {"success": False, "error": {"code": 400, "message": "Uom already exists"}}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = {"success": False, "error": {"code": 400, "message": uom_category.errors}}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_uom_category(request, slug):
    try:
        uom_category = UomCategory.objects.filter(company=request.user.company).get(slug=slug)
    except UomCategory.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    operation = uom_category.delete()
    if operation:
        data = {"success": True}
        st = status.HTTP_200_OK
    else:
        data = {"success": False, "error": {"code": 500, "message": "internal server error"}}
        st = status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(data=data, status=st)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_uom(request, slug):
    try:
        uom = Uom.objects.filter(company=request.user.company).get(slug=slug)
    except Uom.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    operation = uom.delete()
    if operation:
        data = {"success": True}
        st = status.HTTP_200_OK
    else:
        data = {"success": False, "message": "internal server error"}
        st = status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(data=data, status=st)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_view_uom_category(request, slug):
    try:
        uom_category = UomCategory.objects.filter(company=request.user.company).get(slug=slug)
    except UomCategory.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    serializer = UomCategorySerializer(uom_category, many=False)
    data = {"success": True, "data": serializer.data}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_view_uom(request, slug):
    try:
        uom = Uom.objects.filter(company=request.user.company).get(slug=slug)
    except Uom.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    serializer = UomSerializer(uom, many=False)
    data = {"success": True, "data": serializer.data}
    return Response(data, status=status.HTTP_200_OK)


class CategoriesListView(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_fields = ('id', 'slug',)
    ordering_fields = ('name',)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        company = self.request.user.company
        return Category.objects.filter(company=company)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            data = {"success": True, "data": serializer.data, "count": paginated_response.data["count"]}
            return Response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = {"success": True, "data": serializer.data}
        return Response(data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_add_category(request):
    category_serializer = CategorySerializer(data=request.data)
    if category_serializer.is_valid():
        try:
            category_serializer.save(company=request.user.company, created_by=request.user)
            data = {"success": True, "data": category_serializer.data}
            return Response(data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            data = {"success": False, "error": {"code": 400, "message": "Category already exists"}}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = {"success": False, "error": {"code": 400, "message": category_serializer.errors}}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', ])
@permission_classes((IsAuthenticated,))
def api_update_category(request, slug):
    try:
        cateogry = Category.objects.filter(company=request.user.company).get(slug=slug)
    except Category.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        partial = False
    elif request.method == 'PATCH':
        partial = True
    category_serializer = CategorySerializer(cateogry, data=request.data, context={'request': request},
                                             partial=partial)
    if category_serializer.is_valid():
        try:
            category_serializer.save(last_updated_by=request.user)
        except IntegrityError:
            data = {"success": False, "error": {"code": 400, "message": "Category already exists"}}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        data = {"success": True, "data": category_serializer.data}
        return Response(data, status=status.HTTP_200_OK)
    else:
        data = {"success": False, "error": {"code": 400, "message": category_serializer.errors}}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_category(request, slug):
    try:
        category = Category.objects.filter(company=request.user.company).get(slug=slug)
    except Category.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    operation = category.delete()
    if operation:
        data = {"success": True}
        st = status.HTTP_200_OK
    else:
        data = {"success": False, "error": {"code": 500, "message": "internal server error"}}
        st = status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(data=data, status=st)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_view_category(request, slug):
    try:
        category = Category.objects.filter(company=request.user.company).get(slug=slug)
    except Category.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    serializer = CategorySerializer(category, many=False)
    data = {"success": True, "data": serializer.data}
    return Response(data, status=status.HTTP_200_OK)


class BrandsListView(ListAPIView):
    serializer_class = BrandSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (OrderingFilter,)
    ordering_fields = ('name',)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        company = self.request.user.company
        return Brand.objects.filter(company=company)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            data = {"success": True, "data": serializer.data, "count": paginated_response.data["count"]}
            return Response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = {"success": True, "data": serializer.data}
        return Response(data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_add_brand(request):
    brand_serializer = BrandSerializer(data=request.data)
    if brand_serializer.is_valid():

        try:
            brand_serializer.save(company=request.user.company, created_by=request.user)
            data = {"success": True, "data": brand_serializer.data}
            return Response(data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            data = {"success": False, "error": {"code": 400, "message": "Brand already exists"}}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = {"success": False, "error": {"code": 400, "message": brand_serializer.errors}}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', ])
@permission_classes((IsAuthenticated,))
def api_update_brand(request, slug):
    try:
        brand = Brand.objects.filter(company=request.user.company).get(slug=slug)
    except Brand.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        partial = False
    elif request.method == 'PATCH':
        partial = True
    brand_serializer = BrandSerializer(brand, data=request.data, context={'request': request},
                                       partial=partial)
    if brand_serializer.is_valid():
        try:
            brand_serializer.save(last_updated_by=request.user)
        except IntegrityError:
            data = {"success": False, "error": {"code": 400, "message": "brand already exists"}}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        data = {"success": True, "data": brand_serializer.data}
        return Response(data, status=status.HTTP_200_OK)
    else:
        data = {"success": False, "error": {"code": 400, "message": brand_serializer.errors}}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_brand(request, slug):
    try:
        brand = Brand.objects.filter(company=request.user.company).get(slug=slug)
    except Brand.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    operation = brand.delete()
    if operation:
        data = {"success": True}
        st = status.HTTP_200_OK
    else:
        data = {"success": False, "error": {"code": 500, "message": "internal server error"}}
        st = status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(data=data, status=st)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_view_brand(request, slug):
    try:
        brand = Brand.objects.filter(company=request.user.company).get(slug=slug)
    except Brand.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    serializer = BrandSerializer(brand, many=False)
    data = {"success": True, "data": serializer.data}
    return Response(data, status=status.HTTP_200_OK)


class AttributesListView(ListAPIView):
    serializer_class = AttributeSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_fields = ('name', 'att_type',)
    ordering_fields = ('name',)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        company = self.request.user.company
        return Attribute.objects.filter(company=company)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            data = {"success": True, "data": serializer.data, "count": paginated_response.data["count"]}
            return Response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = {"success": True, "data": serializer.data}
        return Response(data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_add_attribute(request):
    attribute_serializer = AttributeSerializer(data=request.data)
    if attribute_serializer.is_valid():
        try:
            attribute_serializer.save(company=request.user.company, created_by=request.user)
            data = {"success": True, "data": attribute_serializer.data}
            return Response(data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            data = {"success": False, "error": {"code": 400, "message": "Attribute and Attribute type already exist"}}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = {"success": False, "error": {"code": 400, "message": attribute_serializer.errors}}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', ])
@permission_classes((IsAuthenticated,))
def api_update_attribute(request, slug):
    try:
        attribute = Attribute.objects.filter(company=request.user.company).get(slug=slug)
    except Attribute.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        partial = False
    elif request.method == 'PATCH':
        partial = True
    attribute_serializer = AttributeSerializer(attribute, data=request.data, context={'request': request},
                                               partial=partial)
    if attribute_serializer.is_valid():
        try:
            attribute_serializer.save(last_updated_by=request.user)
        except IntegrityError:
            data = {"success": False, "error": {"code": 400, "message": "Attribute and Attribute type already exist"}}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        data = {"success": True, "data": attribute_serializer.data}
        return Response(data, status=status.HTTP_200_OK)
    else:
        data = {"success": False, "error": {"code": 400, "message": attribute_serializer.errors}}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_attribute(request, slug):
    try:
        attribute = Attribute.objects.filter(company=request.user.company).get(slug=slug)
    except Attribute.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    operation = attribute.delete()
    if operation:
        data = {"success": True}
        st = status.HTTP_200_OK
    else:
        data = {"success": False, "error": {"code": 500, "message": "internal server error"}}
        st = status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(data=data, status=st)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_view_attribute(request, slug):
    try:
        attribute = Attribute.objects.filter(company=request.user.company).get(slug=slug)
    except Attribute.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    serializer = AttributeSerializer(attribute, many=False)
    data = {"success": True, "data": serializer.data}
    return Response(data, status=status.HTTP_200_OK)


class StokeTakeListView(ListAPIView):
    serializer_class = StokeTakeSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_fields = ('id', 'name', 'type', 'date', 'status', 'slug',)
    ordering_fields = ('name', 'date',)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        company = self.request.user.company
        return StokeTake.objects.filter(company=company)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            data = {"success": True, "data": serializer.data, "count": paginated_response.data["count"]}
            return Response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = {"success": True, "data": serializer.data}
        return Response(data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_add_stoke(request):
    stoke_serializer = StokeTakeSerializer(data=request.data)
    if stoke_serializer.is_valid():
        try:
            instance = stoke_serializer.save(company=request.user.company, created_by=request.user)
        except IntegrityError:
            data = {"success": False, "error": {"code": 400, "message": "Stoke Take already exist"}}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        type = stoke_serializer.validated_data["type"]
        items = []
        location = stoke_serializer.validated_data["location"]
        if type == 'location':
            inventory_balance = Inventory_Balance.objects.filter(location=location)
            for record in inventory_balance:
                items.append(record.item)
        elif type == 'category':
            category = stoke_serializer.validated_data["category"]
            descendants = Category.objects.get(name=category).get_descendants(include_self=True)
            products = Product.objects.filter(Q(category__parent__in=descendants) | Q(category__in=descendants))
            myitems = Item.objects.filter(product__in=products)
            inventory_balance = Inventory_Balance.objects.filter(location=location, item__in=myitems)
            for record in inventory_balance:
                items.append(record.item)
        elif type == 'random':
            inventory_balance = Inventory_Balance.objects.filter(location=location)
            item_list = []
            for record in inventory_balance:
                item_list.append(record.item)
            number_of_items = stoke_serializer.validated_data["random_number"]
            items = random.sample(item_list, number_of_items)
        entry_list = []
        for item in items:
            entry_list.append(StokeEntry(stoke_take=instance, item=item, created_by=request.user))
        StokeEntry.objects.bulk_create(entry_list)
        data = {"success": True, "data": stoke_serializer.data}
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = {"success": False, "error": {"code": 400, "message": stoke_serializer.errors}}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', ])
@permission_classes((IsAuthenticated,))
def api_update_stoke(request, slug):
    try:
        stoke_take = StokeTake.objects.filter(company=request.user.company).get(slug=slug)
    except StokeTake.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if stoke_take.status != 'Drafted':
        data = {"success": False, "error": {"code": 401,
                                            "message": 'stoke cannot be updated as it is already {}'.format(
                                                stoke_take.status)}}
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'PUT':
        partial = False
    elif request.method == 'PATCH':
        partial = True
    stoke_take_serializer = StokeTakeSerializer(stoke_take, data=request.data, context={'request': request},
                                                partial=partial)
    if stoke_take_serializer.is_valid():
        type = stoke_take_serializer.validated_data.get("type", stoke_take.type)
        location = stoke_take_serializer.validated_data.get("location", stoke_take.location)
        items = []
        try:
            stoke_obj = stoke_take_serializer.save(last_updated_by=request.user)
        except IntegrityError:
            data = {"success": False, "error": {"code": 400, "message": "Stoke name already exists"}}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if type != stoke_take.type or location != stoke_take.location.id:
            if type == 'location':
                inventory_balance = Inventory_Balance.objects.filter(location=location)
                for record in inventory_balance:
                    items.append(record.item)
            elif type == 'category':
                category = stoke_take_serializer.validated_data["category"]
                descendants = Category.objects.get(name=category).get_descendants(include_self=True)
                products = Product.objects.filter(Q(category__parent__in=descendants) | Q(category__in=descendants))
                myitems = Item.objects.filter(product__in=products)
                inventory_balance = Inventory_Balance.objects.filter(location=location, item__in=myitems)
                for record in inventory_balance:
                    items.append(record.item)
            elif type == 'random':
                inventory_balance = Inventory_Balance.objects.filter(location=location)
                item_list = []
                for record in inventory_balance:
                    item_list.append(record.item)
                number_of_items = stoke_take_serializer.validated_data["random_number"]
                items = random.sample(item_list, number_of_items)
            entry_list = []
            for item in items:
                entry_list.append(StokeEntry(stoke_take=stoke_take, item=item, created_by=request.user))

            stoke_entry_instances = StokeEntry.objects.filter(stoke_take=stoke_obj)
            stoke_entry_instances.delete()
            StokeEntry.objects.bulk_create(entry_list)
        data = {"success": True, "data": stoke_take_serializer.data}
        return Response(data, status=status.HTTP_200_OK)
    else:
        data = {"success": False, "error": {"code": 400, "message": stoke_take_serializer.errors}}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_stoke(request, slug):
    try:
        stoke_take = StokeTake.objects.filter(company=request.user.company).get(slug=slug)
    except StokeTake.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if stoke_take.status != 'Drafted':
        data = {"success": False, "error": {"code": 401,
                                            "message": 'stoke cannot be deleted as it is already {}'.format(
                                                stoke_take.status)}}
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)
    operation = stoke_take.delete()
    if operation:
        data = {"success": True}
        st = status.HTTP_200_OK
    else:
        data = {"success": False, "error": {"code": 500, "message": "internal server error"}}
        st = status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(data=data, status=st)


class StokeEntryListView(ListAPIView):
    serializer_class = StokeEntrySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_fields = ('item',)
    ordering_fields = ('stoke_take', 'item',)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return StokeEntry.objects.filter(stoke_take__company=self.request.user.company,
                                         stoke_take__slug=self.kwargs['slug'])

    def list(self, request, *args, **kwargs):
        try:
            StokeTake.objects.filter(company=request.user.company).get(slug=self.kwargs['slug'])
        except StokeTake.DoesNotExist:
            data = {"success": False, "error": {"code": 404, "message": "Stoke take not found"}}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            data = {"success": True, "data": serializer.data, "count": paginated_response.data["count"]}
            return Response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = {"success": True, "data": serializer.data}
        return Response(data)


@api_view(['PATCH', ])
@permission_classes((IsAuthenticated,))
def api_update_stoke_entry(request, slug):
    stoke_entry_serializer = StokeEntrySerializer(data=request.data['entries'], many=True)
    try:
        stoke_take = StokeTake.objects.filter(company=request.user.company).get(slug=slug)
    except StokeTake.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "Requested stoke does not exist"}}
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    if stoke_entry_serializer.is_valid():
        if stoke_take.status == 'Drafted' or stoke_take.status == 'In Progress':
            send_to_approval = request.data.get('approve', None),
            ids_to_update = []
            stokes_entries = StokeEntry.objects.filter(stoke_take=stoke_take).values_list('id', flat=True)
            for entry in request.data['entries']:
                id = entry.get('id')
                ids_to_update.append(id)
            list_entries = list(stokes_entries)
            flag = False
            if all(x in list_entries for x in ids_to_update):
                flag = True
            if not flag:
                data = {"success": False, "error": {"code": 400,
                                                    "message": "Please provide entries ids that only belong to the "
                                                               "specified stoke"}}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                data = {}
                data['success'] = True
                data['data'] = []
                for entry in request.data['entries']:
                    id = entry.get('id')
                    quantity = entry.get('quantity')
                    StokeEntry.objects.filter(id=id).update(quantity=quantity, last_updated_by=request.user)
                    data['data'].append(StokeEntrySerializer(StokeEntry.objects.get(id=id)).data)
                if len(StokeEntry.objects.filter(stoke_take=stoke_take).exclude(quantity=None)) > 0:
                    StokeTake.objects.filter(id=stoke_take.id).update(status='In Progress')
                if send_to_approval[0]:
                    if len(StokeEntry.objects.filter(stoke_take=stoke_take, quantity=None)) != 0:
                        data['approve'] = 'You must fill all quantities'
                    else:

                        StokeTake.objects.filter(id=stoke_take.id).update(status='Pending Approval')
                        data['approve'] = 'Stoke sent to approval'
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {"success": False, "error": {"code": 401,
                                                "message": 'Requested stoke is already {}'.format(stoke_take.status)}}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    else:
        data = {"success": False, "error": {"code": 400, "message": stoke_entry_serializer.errors}}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_approve_or_disapprove_stoke(request, slug):
    try:
        stoke_take = StokeTake.objects.filter(company=request.user.company).get(slug=slug)
    except StokeTake.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "Requested stoke does not exist"}}
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    if stoke_take.status != 'Pending Approval':
        data = {"success": False, "error": {"code": 401, "message": 'Requested stoke is {}'.format(stoke_take.status)}}
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    approve = request.data.get('approve', None)
    if approve == True:
        success = create_stoke_transaction(stoke_take, request.user)
        if success:
            stoke_take.status = 'Approved'
            stoke_take.save()
            data = {"success": True}
            return Response(data, status=status.HTTP_200_OK)

        else:
            data = {"success": False,
                    "error": {"code": 500, "message": 'Stoke is NOT approved,Error in updating inventory'}}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif approve == False:
        stoke_take.status = 'In Progress'
        stoke_take.save()
        data = {"success": True}
        return Response(data, status=status.HTTP_200_OK)

    elif approve is None:
        data = {"success": False,
                "error": {"code": 400, "message": 'Please specify (approve) value'}}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
