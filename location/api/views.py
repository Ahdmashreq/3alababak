from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from location.models import Location

from location.api.serializers import LocationSerializer


# @api_view(['GET', ])
# @permission_classes((IsAuthenticated,))
# def api_list_locations(request):
#     type = request.query_params.get('type', None)
#     print(type)
#     locations = []
#     if type is None:
#         locations = Location.objects.filter(company=request.user.company)
#     elif type == 'w' or type == 's':
#         locations = Location.objects.filter(company=request.user.company, type=type)
#
#     serializer = LocationSerializer(locations, many=True)
#     return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_add_location(request):
    location_serializer = LocationSerializer(data=request.data)
    if location_serializer.is_valid():
        location_serializer.save(company=request.user.company, created_by=request.user)
        data = {"success": True, "data": location_serializer.data}
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = {"success": False, "error": {"code": 400, "message": location_serializer.errors}}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', ])
@permission_classes((IsAuthenticated,))
def api_update_location(request, slug):
    try:
        location = Location.objects.filter(company=request.user.company).get(slug=slug)
    except Location.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        partial = False
    elif request.method == 'PATCH':
        partial = True
    location_serializer = LocationSerializer(location, data=request.data, partial=partial)
    if location_serializer.is_valid():
        location_serializer.save()
        data = {"success": True, "data": location_serializer.data}
        return Response(data, status=status.HTTP_200_OK)
    else:
        data = {"success": False, "error": {"code": 400, "message": location_serializer.errors}}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_location(request, slug):
    try:
        location = Location.objects.filter(company=request.user.company).get(slug=slug)
    except Location.DoesNotExist:
        data = {"success": False, "error": {"code": 400, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    operation = location.delete()
    if operation:
        data = {"success": True}
        return Response(data=data, status=status.HTTP_200_OK)
    else:
        data = {"success": False}
        return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_view_location(request, slug):
    try:
        location = Location.objects.filter(company=request.user.company).get(slug=slug)
    except Location.DoesNotExist:
        data = {"success": False, "error": {"code": 404, "message": "record not found"}}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    serializer = LocationSerializer(location, many=False)
    data = {"success": True, "data": serializer.data}
    return Response(data, status=status.HTTP_200_OK)


# List locations with filter on type field
class LocationListView(ListAPIView):
    serializer_class = LocationSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('type',)
    ordering_fields = ('name',)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        company = self.request.user.company
        return Location.objects.filter(company=company)

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
