from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django_filters import rest_framework
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    AllowAny,
    DjangoModelPermissions,
)

from api.serializers import (
    TagSerializer,
    IngredientSerializer,
    CustomUserSerializer,
    RecipeSerializer,
    FavoriteSerializer,
    FollowSerializer,
)
from food.models import (
    Tag,
    Ingredient,
    Recipe,
    Favorite,
    User,
    Follow,
)
from api.permissions import (
    IsAdminOrReadOnly,
)
from api.filters import IngredientFilter
from api.mixins import CreateListUpdateDestroy


class CustomModelViewSet(viewsets.ModelViewSet):
    """Возвращается код 405 при отсутствии прав."""

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response({"detail": "У вас нет прав для выполнения этого действия."},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().handle_exception(exc)


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def me(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# TODO "Структура ответа должна соответствовать ожидаемой"
class TagViewSet(CustomModelViewSet):
    """ViewSet для сериализатора CategorySerializer."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(CustomModelViewSet):
    """ViewSet для сериализатора CategorySerializer."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [rest_framework.DjangoFilterBackend, SearchFilter]
    filterset_class = IngredientFilter
    search_fields = ["name"]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def get_recipe(self):
        return get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))

    # def get_queryset(self):
    #     return Favorite.objects.filter(recipe=self.get_recipe(), user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, recipe=self.get_recipe())

    def delete(self, request, *args, **kwargs):
        instance = get_object_or_404(Favorite, recipe=self.get_recipe(), user=request.user)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_author(self):
        return get_object_or_404(User, pk=self.kwargs.get('user_id'))

    def get_queryset(self):
        return Follow.objects.filter(author=self.get_author(), user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, author=self.get_author())
