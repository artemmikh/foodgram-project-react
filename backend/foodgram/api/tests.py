from django.urls import reverse
from rest_framework.test import APITransactionTestCase
from rest_framework.authtoken.models import Token

from food.models import User, Recipe, Ingredient, RecipeIngredient


class RecipesApiTestCase(APITransactionTestCase):
    """Тесты api рецептов."""

    @classmethod
    def setUpClass(cls):
        cls.url = reverse('recipe-list')

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='vi')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.recipe = Recipe.objects.create(
            author=self.user,
            name='Cookie',
            text='Badabada',
        )
        self.salt = Ingredient.objects.create(
            name='Salt',
            measurement_unit='kg',
        )
        self.recipe_ing = RecipeIngredient.objects.create(
            ingredient=self.salt,
            amount=32,
            recipe=self.recipe
        )
