from rest_framework import viewsets
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

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
from api.permissions import (
    IsAdminOrReadOnly,
)


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def me(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# TODO "Структура ответа должна соответствовать ожидаемой"
class TagViewSet(viewsets.ModelViewSet):
    """ViewSet для сериализатора CategorySerializer."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)

    # нужен чтобы возвращался код 405 при отсутствии доступа
    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response({"detail": "У вас нет прав для выполнения этого действия."},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().handle_exception(exc)


class IngredientViewSet(viewsets.ModelViewSet):
    """ViewSet для сериализатора CategorySerializer."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
