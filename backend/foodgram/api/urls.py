from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from api.views import (
    TagViewSet,
    IngredientViewSet,
    CustomUserViewSet,
    CustomUserViewMe,
)

router_v1 = DefaultRouter()
router_v1.register('tags', TagViewSet)
router_v1.register('ingredients', IngredientViewSet)

urlpatterns = [
    # path('users/', CustomUserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('users/<int:id>/', CustomUserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
    path('api/users/me/', CustomUserViewMe.as_view(), name='user-me'),
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('api-token-auth/', views.obtain_auth_token),

]
