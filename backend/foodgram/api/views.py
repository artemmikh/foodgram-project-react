from django.shortcuts import get_object_or_404
from django_filters import rest_framework
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from djoser.views import UserViewSet

from api.serializers import (
    TagSerializer,
    CustomUserSerializer,
    RecipeSerializer,
    FavoriteSerializer,
    FollowSerializer,
    ShoppingCartSerializer,
    IngredientListSerializer,
)
from food.models import (
    Tag,
    Ingredient,
    Recipe,
    Favorite,
    User,
    Follow,
    ShoppingCart,
)
from api.permissions import (
    IsAdminOrReadOnly,
    IsAuthorOrReadOnly,
)
from api.filters import IngredientFilter, RecipeFilter
from api.pagination import CustomPageNumberPaginator
from api.utils import generate_shopping_list


class CustomModelViewSet(viewsets.ModelViewSet):
    """Возвращается код 405 при отсутствии прав."""

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response(
                {"detail": "У вас нет прав для выполнения этого действия."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().handle_exception(exc)


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def me(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagViewSet(CustomModelViewSet):
    """ViewSet для сериализатора CategorySerializer."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(CustomModelViewSet):
    """ViewSet для сериализатора CategorySerializer."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientListSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [
        rest_framework.DjangoFilterBackend,
        SearchFilter]
    filterset_class = IngredientFilter
    search_fields = ['name']


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def get_recipe(self):
        return get_object_or_404(
            Recipe,
            pk=self.kwargs.get('recipe_id'))

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            recipe=self.get_recipe())

    def delete(self, request, *args, **kwargs):
        user = request.user
        recipe = self.get_recipe()

        if not Favorite.objects.filter(
                user=user,
                recipe=recipe).exists():
            return Response(
                {'detail': 'Этого рецепта нет в избранном'},
                status=status.HTTP_400_BAD_REQUEST)

        instance = get_object_or_404(
            Favorite,
            recipe=self.get_recipe(),
            user=request.user)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPageNumberPaginator

    def get_author(self):
        return get_object_or_404(
            User,
            pk=self.kwargs.get('user_id'))

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            author=self.get_author())

    def delete(self, request, *args, **kwargs):
        user = request.user
        author = self.get_author()

        if not Follow.objects.filter(
                user=user,
                author=author).exists():
            return Response(
                {'detail': 'Подписка не найдена.'},
                status=status.HTTP_400_BAD_REQUEST)

        instance = get_object_or_404(
            Follow,
            user=self.request.user,
            author=self.get_author())
        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated,)

    def get_recipe(self):
        return get_object_or_404(
            Recipe,
            pk=self.kwargs.get('recipe_id'))

    def get_queryset(self):
        return ShoppingCart.objects.filter(
            user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            recipe=self.get_recipe())

    def delete(self, request, *args, **kwargs):
        user = request.user
        recipe = self.get_recipe()

        if not ShoppingCart.objects.filter(
                user=user,
                recipe=recipe).exists():
            return Response(
                {'detail': 'Этого рецепта нет в списке покупок'},
                status=status.HTTP_400_BAD_REQUEST)

        instance = get_object_or_404(
            ShoppingCart,
            recipe=self.get_recipe(),
            user=request.user)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart')
    def create_shopping_list(self, request):
        user = self.request.user

        shopping_list_text = generate_shopping_list(user)

        response = HttpResponse(shopping_list_text, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="Список покупок.txt"')

        return response
