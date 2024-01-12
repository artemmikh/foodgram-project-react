import json
from food.models import Ingredient


def import_ingredients_json():
    json_file_path = '/Users/art/PycharmProjects/foodgram-project-react/data/ingredients.json'
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        ingredients = [Ingredient(name=item['name'], measurement_unit=item['measurement_unit']) for item in data]
        Ingredient.objects.bulk_create(ingredients)

    print("Ингредиенты успешно добавлены в базу данных.")
