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
        return Response(location_serializer.data, status=status.HTTP_201_CREATED)
    return Response(location_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', ])
@permission_classes((IsAuthenticated,))
def api_update_location(request, slug):
    data = {}
    try:
        location = Location.objects.get(slug=slug)
    except Location.DoesNotExist:
        data['failure'] = 'record not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if location.company != request.user.company:
        data['failure'] = 'you are not allowed to edit this location'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'PUT':
        partial = False
    elif request.method == 'PATCH':
        partial = True
    location_serializer = LocationSerializer(location, data=request.data, partial=partial)
    if location_serializer.is_valid():
        location_serializer.save()
        # TODO : find a standardized way to send the response
        data["success"] = 'update successful'
        return Response(location_serializer.data, status=status.HTTP_200_OK)
    return Response(location_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_location(request, slug):
    data = {}
    try:
        location = Location.objects.get(slug=slug)
    except Location.DoesNotExist:
        data['failure'] = 'record not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if location.company != request.user.company:
        data['failure'] = 'you are not allowed to delete this location'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    operation = location.delete()
    if operation:
        data['success'] = 'delete successful'
        st = status.HTTP_200_OK
    else:
        data['failure'] = 'delete failed'
        st = status.HTTP_400_BAD_REQUEST
    return Response(data=data, status=st)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_view_location(request, slug):
    data = {}
    try:
        location = Location.objects.get(slug=slug)
    except Location.DoesNotExist:
        data['failure'] = 'record not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if location.company != request.user.company:
        data['failure'] = 'you are not allowed to view this customer'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    serializer = LocationSerializer(location, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


# List locations with filter on type field
class LocationListView(ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('type',)
    ordering_fields = ('name',)
    pagination_class = PageNumberPagination
