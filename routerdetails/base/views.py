import datetime
import logging

from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status

from .models import router_details
from .serializers import UserSerializerWithToken, RouterSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
        If you want to add data outside token
         """

    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user)

        for key, value in serializer.data.items():
            data[key] = value

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def RetrieveRouterDetails(request):
    router_details_values = router_details.objects.filter(is_delete=False).values()
    logging.info(f"router details fetched successfully at {datetime.datetime.now()}")
    return Response({'message': 'Successfully fetched router details', 'status_code': 200, 'data' : router_details_values}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def InsertRouterDetails(request):
    data = request.data
    router_obj = router_details.objects.create(sapid=data['sapid'], hostname=data['hostname'],
                                               loopback=data['loopback'], macaddress=data['macaddress'])
    logging.info(f"router object with sapid {data['sapid']} created successfully at {datetime.datetime.now()}")
    return Response({'message': 'Successfully created router details', 'status_code': 201})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def UpdateRouterDetails(request):
    data = request.data
    loopback = request.data.get('loopback')
    if not loopback:
        return Response({'message': 'Please provide loopback', 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)
    try:
        router_obj = router_details.objects.get(loopback=loopback, is_delete=False)
    except router_details.DoesNotExist:
        return Response({'message': 'Router of the respective loop back does not exist', 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)
    router_serializer = RouterSerializer(router_obj, data=data, partial=True)
    router_serializer.is_valid(raise_exception=True)
    router_serializer.save()
    logging.info(f"router object with loopbakc {loopback} updated successfully at {datetime.datetime.now()}")
    return Response({'message': 'Successfully updated router details', 'status_code': 201}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteRouterDetails(request):
    data = request.data
    loopback = request.data.get('loopback')
    if not loopback:
        return Response({'message': 'Please provide loopback', 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)
    try:
        router_obj = router_details.objects.get(loopback=loopback)
    except router_details.DoesNotExist:
        return Response({'message': 'Router of the respective loop back does not exist', 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)
    router_obj.is_delete = True
    router_obj.save()
    logging.info(f"router object with loopback {loopback} deleted successfully at {datetime.datetime.now()}")
    return Response({'message': 'Successfully deleted router details', 'status_code': 200},
                    status=status.HTTP_200_OK)
