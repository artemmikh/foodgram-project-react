from django.contrib import admin
from django.db.models import Count

from food.models import (
    Recipe,
    Tag,
    Ingredient,
    ShoppingCart,
    Favorite,
    Follow,
    RecipeIngredient,
)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Административная панель для управления объектами модели Recipe.
    """

    list_display = ('name', 'author', 'favorite_count',)
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags',)
    empty_value_display = '-пусто-'

    def get_queryset(self, request):
        queryset = super().get_queryset(request).annotate(favorite_count=Count('favorite'))
        return queryset

    def favorite_count(self, obj):
        return obj.favorite_count

    favorite_count.short_description = 'В избранном'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """
    Административная панель для управления объектами модели Ingredient.
    """

    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Tag, ShoppingCart, Favorite, Follow, RecipeIngredient)
class PersonAdmin(admin.ModelAdmin):
    pass
