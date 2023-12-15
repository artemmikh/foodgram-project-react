from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    INGREDIENT_CHOICES = [
        # возможно нужно поменять местами англ и рус
        ('salt', 'Соль'),
        ('pepper', 'Перец'),
        ('sugar', 'Сахар'),
        ('flour', 'Мука'),
        ('butter', 'Масло'),
        ('onion', 'Лук'),
        ('garlic', 'Чеснок'),
        ('tomato', 'Помидор'),
        ('chicken', 'Курица'),
        ('beef', 'Говядина'),
    ]
    name = models.CharField(
        max_length=256,
        choices=INGREDIENT_CHOICES,
        verbose_name='Ингредиент'
    )


class Tag(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Тег'
    )
    color = models.CharField(
        max_length=16,
        verbose_name='Цвет в HEX-формате',
        default='#FFFFFF'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг тега')


class Recipe(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Рецепт'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='author_reviews',
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None,
        verbose_name='Картинка'
    )
    description = models.TextField(
        null=True,
        verbose_name='Описание'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    preparation_time_minutes = models.PositiveSmallIntegerField(
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


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиента'
    )
    UNIT_CHOICES = [
        ('g', 'грамм'),
        ('ml', 'миллилитр'),
        ('pcs', 'штука'),
        ('tbsp', 'столовая ложка'),
        ('to taste', 'по вкусу'),
        ('pinch', 'щепотка'),
    ]
    unit_of_measurement = models.CharField(
        max_length=50,
        choices=UNIT_CHOICES,
        verbose_name='Единица измерения'
    )


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
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

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
        verbose_name='Рецепт'
    )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )
    recipes = models.ManyToManyField(
        Recipe,
        verbose_name='Рецепты в списке покупок',
        blank=True
    )


# class RecipeTag(models.Model):
#     pass
# в Django использование ManyToManyField сразу в модели
# позволяет фреймворку автоматически создавать промежуточную
# таблицу для управления отношением многие ко многим.
# Промежуточная таблица создается скрытым образом,
# и вам не нужно явно создавать ее модель, если вы не
# планируете добавлять к ней дополнительные поля.
