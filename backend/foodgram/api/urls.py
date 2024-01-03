from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from djoser.views import UserViewSet

from api.views import (
    TagViewSet,
    IngredientViewSet,
    CustomUserViewSet,
    RecipeViewSet,
    FavoriteViewSet,
)

router_v1 = DefaultRouter()
router_v1.register('tags', TagViewSet)
router_v1.register('ingredients', IngredientViewSet)
router_v1.register('recipes', RecipeViewSet)
router_v1.register(
    r'recipes/(?P<recipe_id>\d+)/favorite',
    FavoriteViewSet,
    basename='favorite',
)

urlpatterns = [
    path('users/me/', CustomUserViewSet.as_view({'get': 'me'}), name='user-me'),
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    re_path('auth/', include('djoser.urls.authtoken')),
]
