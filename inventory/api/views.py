from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from account.models import Customer, Supplier
from inventory.api.serializers import UomCategorySerializer, UomSerializer, CategorySerializer, BrandSerializer, \
    AttributeSerializer
from rest_framework.permissions import IsAuthenticated

from inventory.models import UomCategory, Uom, Category, Brand, Attribute


class UomCategoriesListView(ListAPIView):
    serializer_class = UomCategorySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (OrderingFilter,)
    ordering_fields = ('name',)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        company = self.request.user.company
        return UomCategory.objects.filter(company=company)


class UomListView(ListAPIView):
    serializer_class = UomSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (OrderingFilter,)
    filter_fields = ('category',)
    ordering_fields = ('name', 'category',)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        company = self.request.user.company
        return Uom.objects.filter(company=company)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_add_uom_category(request):
    uom_category_serializer = UomCategorySerializer(data=request.data)
    if uom_category_serializer.is_valid():
        try:
            uom_category_serializer.save(company=request.user.company, created_by=request.user)
            return Response(uom_category_serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            data = {}
            data["failure"] = "Category already exists"
            return Response(data, status=status.HTTP_201_CREATED)
    return Response(uom_category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_add_uom(request):
    uom_serializer = UomSerializer(data=request.data)
    if uom_serializer.is_valid():
        try:
            uom_serializer.save(company=request.user.company, created_by=request.user)
            return Response(uom_serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            data = {}
            data["failure"] = "Uom already exists in this category"
            return Response(data, status=status.HTTP_201_CREATED)
    return Response(uom_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', ])
@permission_classes((IsAuthenticated,))
def api_update_uom_category(request, slug):
    data = {}
    try:
        uom_cateogry = UomCategory.objects.get(slug=slug)
    except UomCategory.DoesNotExist:
        data['failure'] = 'record not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if uom_cateogry.company != request.user.company:
        data['failure'] = 'you are not allowed to edit this category'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'PUT':
        partial = False
    elif request.method == 'PATCH':
        partial = True
    uom_category_serializer = UomCategorySerializer(uom_cateogry, data=request.data, context={'request': request},
                                                    partial=partial)
    if uom_category_serializer.is_valid():
        uom_category_serializer.save()
        # TODO : find a standardized way to send the response
        data["success"] = 'update successful'
        return Response(uom_category_serializer.data, status=status.HTTP_200_OK)
    return Response(uom_category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', ])
@permission_classes((IsAuthenticated,))
def api_update_uom(request, slug):
    data = {}
    try:
        uom = Uom.objects.get(slug=slug)
    except Uom.DoesNotExist:
        data['failure'] = 'record not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if uom.company != request.user.company:
        data['failure'] = 'you are not allowed to edit this category'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'PUT':
        partial = False
    elif request.method == 'PATCH':
        partial = True
    uom_category = UomSerializer(uom, data=request.data, context={'request': request},
                                 partial=partial)
    if uom_category.is_valid():
        uom_category.save()
        # TODO : find a standardized way to send the response
        data["success"] = 'update successful'
        return Response(uom_category.data, status=status.HTTP_200_OK)
    return Response(uom_category.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_uom_category(request, slug):
    data = {}
    try:
        uom_category = UomCategory.objects.get(slug=slug)
    except UomCategory.DoesNotExist:
        data['failure'] = 'record not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if uom_category.company != request.user.company:
        data['failure'] = 'you are not allowed to delete this uom category'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    operation = uom_category.delete()
    if operation:
        data['success'] = 'delete successful'
        st = status.HTTP_200_OK
    else:
        data['failure'] = 'delete failed'
        st = status.HTTP_400_BAD_REQUEST
    return Response(data=data, status=st)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_uom(request, slug):
    data = {}
    try:
        uom = Uom.objects.get(slug=slug)
    except Uom.DoesNotExist:
        data['failure'] = 'record not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if uom.company != request.user.company:
        data['failure'] = 'you are not allowed to delete this uom'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    operation = uom.delete()
    if operation:
        data['success'] = 'delete successful'
        st = status.HTTP_200_OK
    else:
        data['failure'] = 'delete failed'
        st = status.HTTP_400_BAD_REQUEST
    return Response(data=data, status=st)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_view_uom_category(request, slug):
    data = {}
    try:
        uom_category = UomCategory.objects.get(slug=slug)
    except UomCategory.DoesNotExist:
        data['failure'] = 'record not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if uom_category.company != request.user.company:
        data['failure'] = 'you are not allowed to view this category'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    serializer = UomCategorySerializer(uom_category, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_view_uom(request, slug):
    data = {}
    try:
        uom = Uom.objects.get(slug=slug)
    except Uom.DoesNotExist:
        data['failure'] = 'record not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if uom.company != request.user.company:
        data['failure'] = 'you are not allowed to view this category'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    serializer = UomSerializer(uom, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


class CategoriesListView(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (OrderingFilter,)
    ordering_fields = ('name',)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        company = self.request.user.company
        return Category.objects.filter(company=company)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_add_category(request):
    category_serializer = CategorySerializer(data=request.data)
    if category_serializer.is_valid():
        try:
            category_serializer.save(company=request.user.company, created_by=request.user)
            return Response(category_serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            data = {}
            data["failure"] = "Category already exists"
            return Response(data, status=status.HTTP_201_CREATED)
    return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', ])
@permission_classes((IsAuthenticated,))
def api_update_category(request, slug):
    data = {}
    try:
        cateogry = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        data['failure'] = 'record not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if cateogry.company != request.user.company:
        data['failure'] = 'you are not allowed to edit this category'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'PUT':
        partial = False
    elif request.method == 'PATCH':
        partial = True
    category_serializer = CategorySerializer(cateogry, data=request.data, context={'request': request},
                                             partial=partial)
    if category_serializer.is_valid():
        category_serializer.save()
        # TODO : find a standardized way to send the response
        data["success"] = 'update successful'
        return Response(category_serializer.data, status=status.HTTP_200_OK)
    return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_category(request, slug):
    data = {}
    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        data['failure'] = 'record not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if category.company != request.user.company:
        data['failure'] = 'you are not allowed to delete this uom category'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    operation = category.delete()
    if operation:
        data['success'] = 'delete successful'
        st = status.HTTP_200_OK
    else:
        data['failure'] = 'delete failed'
        st = status.HTTP_400_BAD_REQUEST
    return Response(data=data, status=st)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_view_category(request, slug):
    data = {}
    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        data['failure'] = 'record not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if category.company != request.user.company:
        data['failure'] = 'you are not allowed to view this category'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    serializer = CategorySerializer(category, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


class BrandsListView(ListAPIView):
    serializer_class = BrandSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (OrderingFilter,)
    ordering_fields = ('name',)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        company = self.request.user.company
        return Brand.objects.filter(company=company)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_add_brand(request):
    brand_serializer = BrandSerializer(data=request.data)
    if brand_serializer.is_valid():
        try:
            brand_serializer.save(company=request.user.company, created_by=request.user)
            return Response(brand_serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            data = {}
            data["failure"] = "Brand already exists"
            return Response(data, status=status.HTTP_201_CREATED)
    return Response(brand_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', ])
@permission_classes((IsAuthenticated,))
def api_update_brand(request, slug):
    data = {}
    try:
        brand = Brand.objects.get(slug=slug)
    except Brand.DoesNotExist:
        data['failure'] = 'record not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if brand.company != request.user.company:
        data['failure'] = 'you are not allowed to edit this brand'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'PUT':
        partial = False
    elif request.method == 'PATCH':
        partial = True
    brand_serializer = BrandSerializer(brand, data=request.data, context={'request': request},
                                       partial=partial)
    if brand_serializer.is_valid():
        brand_serializer.save()
        # TODO : find a standardized way to send the response
        data["success"] = 'update successful'
        return Response(brand_serializer.data, status=status.HTTP_200_OK)
    return Response(brand_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_brand(request, slug):
    data = {}
    try:
        brand = Brand.objects.get(slug=slug)
    except Brand.DoesNotExist:
        data['failure'] = 'record not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if brand.company != request.user.company:
        data['failure'] = 'you are not allowed to delete this brand'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    operation = brand.delete()
    if operation:
        data['success'] = 'delete successful'
        st = status.HTTP_200_OK
    else:
        data['failure'] = 'delete failed'
        st = status.HTTP_400_BAD_REQUEST
    return Response(data=data, status=st)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_view_brand(request, slug):
    data = {}
    try:
        brand = Brand.objects.get(slug=slug)
    except Brand.DoesNotExist:
        data['failure'] = 'record not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if brand.company != request.user.company:
        data['failure'] = 'you are not allowed to view this brand'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    serializer = BrandSerializer(brand, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


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


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_add_attribute(request):
    attribute_serializer = AttributeSerializer(data=request.data)
    if attribute_serializer.is_valid():
        try:
            attribute_serializer.save(company=request.user.company, created_by=request.user)
            return Response(attribute_serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            data = {}
            data["failure"] = "Attribute and Attribute type already exist"
            return Response(data, status=status.HTTP_201_CREATED)
    return Response(attribute_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', ])
@permission_classes((IsAuthenticated,))
def api_update_attribute(request, slug):
    data = {}
    try:
        attribute = Attribute.objects.get(slug=slug)
    except Attribute.DoesNotExist:
        data['failure'] = 'record not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if attribute.company != request.user.company:
        data['failure'] = 'you are not allowed to edit this brand'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'PUT':
        partial = False
    elif request.method == 'PATCH':
        partial = True
    attribute_serializer = AttributeSerializer(attribute, data=request.data, context={'request': request},
                                               partial=partial)
    if attribute_serializer.is_valid():
        attribute_serializer.save()
        # TODO : find a standardized way to send the response
        data["success"] = 'update successful'
        return Response(attribute_serializer.data, status=status.HTTP_200_OK)
    return Response(attribute_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_attribute(request, slug):
    data = {}
    try:
        attribute = Attribute.objects.get(slug=slug)
    except Attribute.DoesNotExist:
        data['failure'] = 'record not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if attribute.company != request.user.company:
        data['failure'] = 'you are not allowed to delete this attribute'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    operation = attribute.delete()
    if operation:
        data['success'] = 'delete successful'
        st = status.HTTP_200_OK
    else:
        data['failure'] = 'delete failed'
        st = status.HTTP_400_BAD_REQUEST
    return Response(data=data, status=st)

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_view_attribute(request, slug):
    data = {}
    try:
        attribute = Attribute.objects.get(slug=slug)
    except Attribute.DoesNotExist:
        data['failure'] = 'record not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if attribute.company != request.user.company:
        data['failure'] = 'you are not allowed to view this attribute'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    serializer = AttributeSerializer(attribute, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)