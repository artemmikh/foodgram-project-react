from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator)

User = get_user_model()

MIN_COOKING_TIME = 1
MAX_COOKING_TIME = 10000
MIN_AMOUNT = 1
MAX_AMOUNT = 10000


class Ingredient(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Ингредиент'
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единица измерения',
        default='г'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Тег',
        unique=True
    )
    color = models.CharField(
        max_length=16,
        verbose_name='Цвет в HEX-формате',
        default='#FFFFFF'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг тега')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.slug


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Рецепт'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='author_recipe',
    )
    image = models.ImageField(
        upload_to='',
        verbose_name='Картинка',
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                MIN_COOKING_TIME,
                message='Время приготовления не может быть меньше 1.'),
            MaxValueValidator(
                MAX_COOKING_TIME,
                message='Время приготовления не может быть больше 10000.')],
        verbose_name='Время приготовления в минутах'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe_ingredient',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='recipe_ingredient',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиента',
        validators=[
            MinValueValidator(
                MIN_AMOUNT,
                message='Количество ингредиента не может быть меньше 1.'),
            MaxValueValidator(
                MAX_AMOUNT,
                message='Количество ингредиента не может быть больше 10000.'),
        ]
    )

    class Meta:
        verbose_name = 'Рецепт-ингредиент'
        verbose_name_plural = 'Рецепт-ингредиент'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Пользователь, на которого подписываются'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow')
        ]

    def __str__(self):
        return f'{self.user}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorited_by'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite')
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепты в списке покупок',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart')
        ]
