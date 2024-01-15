from django.db.models import Sum

from food.models import RecipeIngredient


def generate_shopping_list(user):
    shopping_list_items = (
        RecipeIngredient.objects
        .filter(recipe__shoppingcart__user=user)
        .values('ingredient__name', 'ingredient__measurement_unit')
        .annotate(amount=Sum('amount'))
    )

    shopping_list_text = ''
    for item in shopping_list_items:
        shopping_list_text += (
            f"{item['ingredient__name']} "
            f"({item['ingredient__measurement_unit']}) "
            f"— {item['amount']}\n"
        )

    return shopping_list_text
