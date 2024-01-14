import json
from food.models import Ingredient, Tag, User


def import_ingredients_json():
    json_file_path = 'food/data/ingredients.json'
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        ingredients = [Ingredient(
            name=item['name'],
            measurement_unit=item['measurement_unit']) for item in data]
        Ingredient.objects.bulk_create(ingredients)

    print("Ингредиенты успешно добавлены в базу данных.")


def import_tags_to_bd():
    tags_data = [
        {'name': 'Завтрак', 'color': '#FF0000', 'slug': 'slugname1'},
        {'name': 'Обед', 'color': '#00FF00', 'slug': 'slugname2'},
        {'name': 'Ужин', 'color': '#0000FF', 'slug': 'slugname3'}
    ]

    tags = [Tag(
        name=item['name'],
        color=item['color'],
        slug=item['slug']
    ) for item in tags_data]

    Tag.objects.bulk_create(tags)

    print("Теги успешно добавлены в базу данных.")


def del_for_test_postman():
    # RecipeIngredient.objects.all().delete()
    # Recipe.objects.all().delete()
    # Ingredient.objects.create(name='молоко', measurement_unit='мл')
    # Ingredient.objects.create(name='соль', measurement_unit='мл')
    # Ingredient.objects.create(name='мясо', measurement_unit='г')
    usernames_to_delete = [
        'vasya.pupkin',
        'second-user',
        'third-user-username']
    for username in usernames_to_delete:
        try:
            user_to_delete = User.objects.get(username=username)
            user_to_delete.delete()
            print(f"Пользователь {username} успешно удален.")
        except User.DoesNotExist:
            print(f"Пользователь {username} не найден.")


def import_ingredients_to_db():
    ingredients_data = [
        {'name': 'Мука', 'measurement_unit': 'г'},
        {'name': 'Сахар', 'measurement_unit': 'г'},
        {'name': 'Яйцо', 'measurement_unit': 'шт'},
        {'name': 'Масло растительное', 'measurement_unit': 'мл'},
        {'name': 'Соль', 'measurement_unit': 'г'},
        {'name': 'Перец черный', 'measurement_unit': 'г'},
        {'name': 'Томаты', 'measurement_unit': 'шт'},
        {'name': 'Огурцы', 'measurement_unit': 'шт'},
        {'name': 'Лук', 'measurement_unit': 'г'},
        {'name': 'Чеснок', 'measurement_unit': 'зубчик'},
        {'name': 'Базилик', 'measurement_unit': 'г'},
    ]

    ingredients = []
    for item in ingredients_data:
        existing_ingredient = Ingredient.objects.filter(
            name=item['name']).first()
        if existing_ingredient:
            print(f"Ингредиент с именем '{item['name']}' уже существует.")
        else:
            new_ingredient = Ingredient(
                name=item['name'],
                measurement_unit=item['measurement_unit']
            )
            ingredients.append(new_ingredient)
    Ingredient.objects.bulk_create(ingredients)
    print("Ингредиенты успешно добавлены в базу данных.")
