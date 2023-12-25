from rest_framework import viewsets
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

from api.serializers import (
    TagSerializer,
    IngredientSerializer,
    CustomUserSerializer
)
from food.models import (
    Tag,
    Ingredient,
    User
)


class CustomUserViewSet(DjoserUserViewSet):
    """Кстомный ViewSet для сериализатора CategorySerializer."""
    permission_classes = (permissions.AllowAny,)

    @action(detail=True, methods=['get'])
    def profile(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class CustomUserViewMe(DjoserUserViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class TagViewSet(viewsets.ModelViewSet):
    """ViewSet для сериализатора CategorySerializer."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    """ViewSet для сериализатора CategorySerializer."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
