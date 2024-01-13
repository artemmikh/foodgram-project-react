import json
from django.utils.text import slugify

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

    tags_data = [
        {'name': 'Завтрак', 'color': '#FF0000'},
        {'name': 'Обед', 'color': '#00FF00'},
        {'name': 'Ужин', 'color': '#0000FF'}
    ]

    tags = [Tag(
        name=item['name'],
        color=item['color'],
        slug=slugify(item['name'])
    ) for item in tags_data]

    Tag.objects.bulk_create(tags)

    print("Теги успешно добавлены в базу данных.")
