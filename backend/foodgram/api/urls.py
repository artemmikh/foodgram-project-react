from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from djoser.views import UserViewSet as DjoserUserViewSet

from api.views import (
    TagViewSet,
    IngredientViewSet,
    CustomUserViewSet,
    CustomUserViewSetMe,
)

router_v1 = DefaultRouter()
router_v1.register('tags', TagViewSet)
router_v1.register('ingredients', IngredientViewSet)
router_v1.register(r'users', DjoserUserViewSet, basename='user')

urlpatterns = [
    # path('users/', CustomUserViewSet.as_view({'get': 'list'}), name='user-list'),
    # path('users/<int:id>/', CustomUserViewSetMe.as_view({'get': 'retrieve'}), name='user-detail'),
    path('api/users/me/', CustomUserViewSetMe.as_view({'get': 'retrieve', 'patch': 'partial_update'}),
         name='user-me'),
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('token/login/', views.obtain_auth_token),
]
