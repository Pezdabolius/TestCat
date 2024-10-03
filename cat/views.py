from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import Kitten
from .serializers import KittenSerializer
from .permission import IsOwner
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method='get',
    operation_description="Получения списка котят. Фильтрация по породе.",
    manual_parameters=[
        openapi.Parameter('breed', openapi.IN_QUERY, description="Breed of the kitten", type=openapi.TYPE_STRING),
    ],
    responses={
        200: openapi.Response('A list of kittens', KittenSerializer(many=True)),
    },
)
@swagger_auto_schema(
    method='post',
    operation_description="Создание котёнка.",
    request_body=KittenSerializer,
    responses={
        201: openapi.Response('Kitten created', KittenSerializer),
        400: 'Invalid input',
    },
)
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


@swagger_auto_schema(
    method='get',
    operation_description="Получения списка пород.",
    responses={
        200: openapi.Response('A list of kittens', KittenSerializer(many=True)),
    },
)
@api_view(['GET'])
def list_breed(request):
    if request.method == 'GET':
        response_data = {
            'breeds': [breed for breed in Kitten.objects.values_list('breed', flat=True)]
        }
        return Response(response_data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_description="Получения детальной информации о котёнке",
    responses={
        200: openapi.Response('Kitten detail', KittenSerializer),
        404: 'Kitten not found',
    },
)
@swagger_auto_schema(
    method='put',
    operation_description="Обновление информации о котёнке",
    manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
        ],
    request_body=KittenSerializer,
    responses={
        200: openapi.Response('Updated kitten details', KittenSerializer),
        400: 'Invalid input',
        403: 'Permission denied',
        404: 'Kitten not found',
    },
)
@swagger_auto_schema(
    method='patch',
    operation_description="Частичное обновление информации о котёнке",
    manual_parameters=[
                openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
            ],
    request_body=KittenSerializer,
    responses={
        200: openapi.Response('Updated kitten details', KittenSerializer),
        400: 'Invalid input',
        403: 'Permission denied',
        404: 'Kitten not found',
    },
)
@swagger_auto_schema(
    method='delete',
    operation_description="Удаление котёнке",
    manual_parameters=[
                openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
            ],
    request_body=KittenSerializer,
    responses={
        204: 'Kitten deleted',
        403: 'Permission denied',
        404: 'Kitten not found',
    },
)
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsOwner])
def kitten_detail(request, pk):
    try:
        queryset = Kitten.objects.get(pk=pk)
    except Kitten.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method in ['PUT', 'PATCH', 'DELETE']:
        if not IsOwner().has_object_permission(request, None, queryset):
            return Response(status=status.HTTP_403_FORBIDDEN)

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
