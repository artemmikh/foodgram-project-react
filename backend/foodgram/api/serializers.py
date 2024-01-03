from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer

from food.models import (
    Recipe,
    Tag,
    Ingredient,
    ShoppingCart,
    Favorite,
    Follow,
)
from food.models import Follow


# Обработка картинок в сериализаторе
# https://practicum.yandex.ru/learn/python-developer-plus/courses/ff822384-ebee-4c94-b637-107f18eb1678/sprints/147137/topics/1870f483-968b-4853-b51a-c0417384c8dd/lessons/df9057d3-0bf4-4bb1-9a25-ac17d9e52798/


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag."""

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )
        lookup_field = 'slug'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ShoppingCart."""

    # cooking_time =

    class Meta:
        model = ShoppingCart
        fields = (
            'id',
            'name',
            'image',
            # 'cooking_time',
        )


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Favorite."""

    id = serializers.IntegerField(source='recipe.id', read_only=True)
    name = serializers.CharField(source='recipe.name', read_only=True)
    image = serializers.ImageField(source='recipe.image', required=False, read_only=True)
    cooking_time = serializers.IntegerField(source='recipe.cooking_time', read_only=True)

    class Meta:
        model = Favorite
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )

    def validate(self, data):
        user = self.context['request'].user
        recipe = self.context['view'].get_recipe()
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError('Вы уже подписаны на этот рецепт.')
        return data


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Follow."""

    class Meta:
        model = Follow
        fields = ()


class CustomRegisterSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Follow.objects.filter(user=request.user, author=obj).exists()
        return False


# TODO допилить два поля
class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe."""

    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            # 'is_favorited',
            # 'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
