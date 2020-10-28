from rest_framework.response import Response
from rest_framework.decorators import api_view
from account.models import Customer, Supplier, Company
from .serializers import UserSerializer


@api_view(['POST', ])
def api_register_user(request):
    serializer = UserSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        comp = Company(
            name=serializer.validated_data['company_name'],
            created_by=user.id,
        )
        comp.save()
        user.company_id = comp.id
        user.is_staff = True
        user.save(update_fields=['company', 'is_staff'])
        data['response'] = "Successfully registered a new user"
        data['username'] = user.username
        data['email'] = user.email

    else:
        data = serializer.errors
    return Response(data)
