from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import (
    TagViewSet,
    IngredientViewSet,
)

router_v1 = DefaultRouter()
router_v1.register('tags', TagViewSet)
router_v1.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
