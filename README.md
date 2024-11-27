# Проект «Рецепты»

Проект «Рецепты» — приложение, с помощью которого пользователи будут
публиковать рецепты, добавлять чужие рецепты в
избранное и
подписываться на публикации других авторов. Пользователям сайта также будет
доступен сервис «Список покупок». Он
позволит создавать список продуктов, которые нужно купить для приготовления
выбранных блюд.
У будущего веб-приложения уже есть готовый фронтенд — это одностраничное
SPA-приложение, написанное на фреймворке React.
Файлы, необходимые для его сборки, хранятся в репозитории
foodgram-project-react в папке frontend.

## Foodgram API

Foodgram API - это часть проекта «Рецепты», который предоставляет API для
работы с рецептами, ингредиентами и списками
покупок. С помощью этого API вы можете создавать, редактировать, просматривать
и удалять рецепты, а также получать
списки покупок на основе ваших рецептов.

## Основные возможности

- **Управление рецептами:** Создание, редактирование, просмотр и удаление
  рецептов.
- **Ингредиенты и теги:** Получение информации об ингредиентах и добавление
  тегов к рецептам.
- **Списки покупок:** Генерация списка покупок на основе выбранных рецептов.
- **Подписки на авторов:** Возможность подписываться на других пользователей и
  следить за их новыми рецептами.

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/artemmikh/foodgram-project-react.git
    ```

2. Создайте и активируйте виртуальное окружение:

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

4. Создайте файл `.env` в корне проекта с таким содержимым:

   ```bash
   POSTGRES_USER=user
   POSTGRES_PASSWORD=password
   POSTGRES_DB=django
   DB_HOST=db
   DB_PORT=5432
   DB_NAME=foodgram_db
   SECRET_KEY=django-insecure-EXAMPLE


5. Примените миграции:

    ```bash
    python manage.py migrate
    ```

6. Запустите сервер:

    ```bash
    python manage.py runserver
    ```

7. Перейдите по адресу [http://localhost:8000/](http://localhost:8000/) в своем
   браузере.

## Использование API

Документация API доступна по
адресу [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/).
Здесь вы найдете
подробную информацию о доступных эндпоинтах, параметрах запросов и примерах.

### Пример использования

Получение списка рецептов:

```bash
GET "http://localhost:8000/api/recipes/"
```

Пример ответа:

```json
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```