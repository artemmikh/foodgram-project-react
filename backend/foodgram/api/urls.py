from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api.views import (
    TagViewSet,
    IngredientViewSet,
    CustomUserViewSet,
    RecipeViewSet,
    FavoriteViewSet,
    FollowViewSet,
    ShoppingCartViewSet,
)

router_v1 = DefaultRouter()
router_v1.register('tags', TagViewSet)
router_v1.register('ingredients', IngredientViewSet)
router_v1.register(
    r'recipes/(?P<recipe_id>\d+)/favorite',
    FavoriteViewSet,
    basename='favorite',
)
router_v1.register(
    r'users/(?P<user_id>\d+)/subscribe',
    FollowViewSet,
    basename='follow',
)
router_v1.register(
    r'users/subscriptions',
    FollowViewSet,
    basename='follow_list',
)
router_v1.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart',
    ShoppingCartViewSet,
    basename='shopping_cart',
)
router_v1.register('recipes', RecipeViewSet)

urlpatterns = [
    path(
        'users/me/',
        CustomUserViewSet.as_view({'get': 'me'}),
        name='user-me'),
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    re_path('auth/', include('djoser.urls.authtoken')),
]
