import base64
from django.core.files.base import ContentFile
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer

from food.models import (
    Recipe,
    Tag,
    Ingredient,
    ShoppingCart,
    Favorite,
    Follow,
    RecipeIngredient,
)


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


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
        read_only_fields = ("__all__",)


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ShoppingCart."""

    id = serializers.IntegerField(source='recipe.id', read_only=True)
    name = serializers.CharField(source='recipe.name', read_only=True)
    image = serializers.ImageField(
        source='recipe.image',
        required=False, read_only=True
    )
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time',
        read_only=True
    )

    class Meta:
        model = ShoppingCart
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )

    def validate(self, data):
        user = self.context['request'].user
        recipe_id = self.context['view'].kwargs.get('recipe_id')

        if not Recipe.objects.filter(pk=recipe_id).exists():
            raise serializers.ValidationError('Рецепт не найден.')

        if ShoppingCart.objects.filter(user=user, recipe=recipe_id).exists():
            raise serializers.ValidationError(
                'Этот рецепт уже в списке покупок.'
            )

        return data


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Favorite."""

    id = serializers.IntegerField(
        source='recipe.id',
        read_only=True
    )
    name = serializers.CharField(
        source='recipe.name',
        read_only=True
    )
    image = serializers.ImageField(
        source='recipe.image',
        required=False, read_only=True
    )
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time',
        read_only=True
    )

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
        recipe_id = self.context['view'].kwargs.get('recipe_id')

        if not Recipe.objects.filter(pk=recipe_id).exists():
            raise serializers.ValidationError(
                'Рецепт не найден.'
            )

        if Favorite.objects.filter(user=user, recipe=recipe_id).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этот рецепт.'
            )

        return data


class RecipeSmallSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe."""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
        read_only_fields = [
            'id',
            'name',
            'image',
            'cooking_time'
        ]


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Follow."""

    email = serializers.EmailField(
        source='author.email',
        read_only=True)
    id = serializers.IntegerField(
        source='author.id',
        read_only=True)
    username = serializers.CharField(
        source='author.username',
        read_only=True)
    first_name = serializers.CharField(
        source='author.first_name',
        read_only=True)
    last_name = serializers.CharField(
        source='author.last_name',
        read_only=True)
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeSmallSerializer(
        many=True,
        read_only=True,
        source='author.author_recipe')
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        read_only_fields = ['user', 'author']

    def validate(self, data):
        user = self.context['request'].user
        author = self.context['view'].get_author()
        if Follow.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя.')
        elif user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя')
        return data

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Follow.objects.filter(
                user=request.user,
                author=obj.author).exists()
        return False

    def get_recipes_count(self, obj):
        return obj.author.author_recipe.count()


class CustomRegisterSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = (
            'id',
            'email',
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
            return Follow.objects.filter(
                user=request.user,
                author=obj).exists()
        return False


class IngredientListSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient."""
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )
        read_only_fields = ['name', 'measurement_unit']

    def get_amount(self, obj):
        try:
            recipe_ingredients = RecipeIngredient.objects.filter(
                ingredient=obj)
            if recipe_ingredients.exists():
                return recipe_ingredients.first().amount
        except RecipeIngredient.DoesNotExist:
            return None


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели RecipeIngredient."""

    id = serializers.IntegerField(write_only=True)
    name = serializers.ReadOnlyField(
        source='ingredient.name',
        read_only=True)
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit', read_only=True
    )

    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe."""

    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )
    ingredients = RecipeIngredientSerializer(many=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate_ingredients(self, value):

        if not value:
            raise serializers.ValidationError(
                'Ингредиенты обязательны для заполнения')
        seen_ingredient_ids = set()
        for ingredient in value:
            ingredient_id = ingredient.get('id')
            amount = ingredient.get('amount')

            if amount is not None and amount < 1:
                raise serializers.ValidationError(
                    'Количество ингредиента не может быть меньше 1.')

            if ingredient_id in seen_ingredient_ids:
                raise serializers.ValidationError(
                    'Ингредиент повторяется в рецепте.')
            seen_ingredient_ids.add(ingredient_id)

            try:
                Ingredient.objects.get(id=ingredient_id)
            except Ingredient.DoesNotExist:
                raise serializers.ValidationError(
                    f'Ингредиент с id {ingredient_id} не существует.')
        return value

    def create(self, validated_data):

        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        self.validate_ingredients(ingredients)

        if len(set(tags)) != len(tags):
            raise serializers.ValidationError(
                'Тег повторяется, так нельзя.')

        if 'image' not in validated_data or validated_data['image'] is None:
            raise serializers.ValidationError(
                'Изображение обязательно нужно добавить')

        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                amount=ingredient['amount'],
                recipe=recipe,
            )
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time)

        tags = validated_data.get('tags')
        if tags:
            if len(set(tags)) != len(tags):
                raise serializers.ValidationError(
                    'Повторяющиеся теги не допускаются.')

            instance.tags.set(tags)
        else:
            raise serializers.ValidationError(
                'Теги обязательны для обновления рецепта.')

        ingredients_data = validated_data.get('ingredients')
        if ingredients_data:
            # уд только те которых нет в новых данных
            current_ingredient_ids = [item['id'] for item in ingredients_data]
            instance.ingredients.exclude(
                id__in=current_ingredient_ids).delete()

            for ingredient_data in ingredients_data:
                ingredient_id = ingredient_data['id']
                amount = ingredient_data['amount']
                ingredient, created = RecipeIngredient.objects.get_or_create(
                    ingredient=Ingredient.objects.get(id=ingredient_id),
                    amount=amount,
                    recipe=instance,
                )
        else:
            raise serializers.ValidationError(
                'Ингредиенты обязательны для обновления рецепта.')
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['tags'] = TagSerializer(
            instance.tags.all(),
            many=True).data
        data['ingredients'] = IngredientSerializer(
            instance.ingredients.all(), many=True
        ).data
        return data

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Favorite.objects.filter(
                user=user,
                recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return ShoppingCart.objects.filter(
                user=user,
                recipe=obj).exists()
        return False
