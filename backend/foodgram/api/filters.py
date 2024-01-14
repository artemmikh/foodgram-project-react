from django_filters import rest_framework
from food.models import Ingredient, Recipe


class IngredientFilter(rest_framework.FilterSet):
    name = rest_framework.CharFilter(
        field_name="name",
        lookup_expr="istartswith"
    )

    class Meta:
        model = Ingredient
        fields = ["name"]


class RecipeFilter(rest_framework.FilterSet):
    tags = rest_framework.AllValuesMultipleFilter(field_name='tags__slug')
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method='filter_is_in_shopping_cart',
    )
    is_favorited = rest_framework.NumberFilter(method="filter_is_favorited")

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_in_shopping_cart', 'is_favorited')

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            if value:
                return queryset.filter(shoppingcart__user=user)
            else:
                return queryset.exclude(shoppingcart__user=user)
        return queryset

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            if value:
                return queryset.filter(author__following__user=user)
            else:
                return queryset.exclude(author__following__user=user)
        return queryset
