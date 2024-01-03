from django.contrib import admin

from food.models import (
    Recipe,
    Tag,
    Ingredient,
    ShoppingCart,
    Favorite,
    Follow,
)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Административная панель для управления объектами модели Recipe.
    """

    list_display = ('pk', 'name', 'image', 'author',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Tag, Ingredient, ShoppingCart, Favorite, Follow)
class PersonAdmin(admin.ModelAdmin):
    pass
