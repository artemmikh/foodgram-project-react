import json

from food.models import Ingredient, Tag


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
        {'name': 'Завтрак', 'color': '#6B8E23', 'slug': 'slugname1'},
        {'name': 'Обед', 'color': '#87CEEB', 'slug': 'slugname2'},
        {'name': 'Ужин', 'color': '##FF8C00', 'slug': 'slugname3'},
        {'name': 'Здоровье', 'color': '#00FF00', 'slug': 'healthy'},
        {'name': 'Быстрый ужин', 'color': '#FFD700', 'slug': 'quick-dinner'},
        {'name': 'Вегетарианское', 'color': '#32CD32', 'slug': 'vegetarian'},
        {'name': 'Экзотика', 'color': '#FF4500', 'slug': 'exotic-cuisine'},
        {'name': 'Десерт', 'color': '#8A2BE2', 'slug': 'dessert'},
        {'name': 'Постное', 'color': '#800080', 'slug': 'fasting'}
    ]

    tags = [Tag(
        name=item['name'],
        color=item['color'],
        slug=item['slug']
    ) for item in tags_data]

    Tag.objects.bulk_create(tags)

    print("Теги успешно добавлены в базу данных.")
