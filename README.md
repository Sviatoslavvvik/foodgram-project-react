# Проект FoodGram  «Продуктовый помощник»
## Описание:
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Установка:
Как запустить проект:

Cоздать и активировать виртуальное окружение:
```
python -m venv venv
```
```
source venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python manage.py migrate
```
Запустить проект:
```
python manage.py runserver
```
## Основные endpoints:
```
"регистрация": "http://localhost/api/users/"
```
```
"получение токена": "http://localhost/api/auth/token/login/"
```
```
"тэги": "http://localhost/api/tags/"
```
```
"рецепты": "http://localhost/api/recipes/"
```
```
"список покупок": "http://localhost/api/recipes/download_shopping_cart/"
```
```
"избранное": "http://localhost/api/recipes/{id}/favorite/"
```
```
"подписки": "http://localhost/api/users/subscriptions/"
```
```
"ингредиенты": "http://localhost/api/ingredients/"
```
## Что использовалось при разработке:
* Django
* Django REST
* Simple JWT
* Docker
* Python 3.7
* nginx

В сети:
51.250.101.206
