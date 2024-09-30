from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .models import Kitten
from .serializers import KittenSerializer
from .permission import IsOwner


@api_view(['GET', 'POST'])
def list_kittens(request):
    if request.method == 'GET':
        queryset = Kitten.objects.all()
        breed = request.query_params.get('breed')
        if breed:
            queryset = queryset.filter(breed=breed)
        serializer = KittenSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = KittenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_breed(request):
    if request.method == 'GET':
        response_data = {
            'breeds': [breed for breed in Kitten.objects.values_list('breed', flat=True)]
        }
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsOwner])
def kitten_detail(request, pk):
    try:
        queryset = Kitten.objects.get(pk=pk)
    except Kitten.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = KittenSerializer(queryset)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = KittenSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = KittenSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
