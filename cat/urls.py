from django.urls import path
from cat import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('kittens/', views.list_kittens),
    path('kittens/<int:pk>/', views.kitten_detail),
    path('breeds/', views.list_breed),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]