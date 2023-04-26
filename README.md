# Foodgram - «Продуктовый помощник»

Cервис, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

#### Пример развернутого проекта можно посмотреть .....158.160.21.33 проверка миграций tot hfp

# Технологии:
    Django==2.2
    Django-rest-framework==3.12.4
    Python==3.8.10
    PostgreSQL
    Docker

# Запуск и работа с проектом
Чтобы развернуть проект, вам потребуется:

## Регистрация и авторизация
В сервисе предусмотрена система регистрации и авторизации пользователей.
Обязательные поля для пользователя:
<li> Логин
<li> Пароль
<li> Email
<li> Имя
<li> Фамилия

## Права доступа к ресурсам сервиса

### неавторизованные пользователи могут:

    - создать аккаунт;
    - просматривать рецепты на главной;
    - просматривать отдельные страницы рецептов;
    - фильтровать рецепты по тегам;

### авторизованные пользователи могут:

    - входить в систему под своим логином и паролем;
    - выходить из системы (разлогиниваться);
    - менять свой пароль;
    - создавать/редактировать/удалять собственные рецепты;
    - просматривать рецепты на главной;
    - просматривать страницы пользователей;
    - просматривать отдельные страницы рецептов;
    - фильтровать рецепты по тегам;
    - работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов;
    - работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл со количеством необходимых ингридиентов для рецептов из списка покупок;
    - подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок;

### администратор
Администратор обладает всеми правами авторизованного пользователя.
<br> Плюс к этому он может:

    - изменять пароль любого пользователя;
    - создавать/блокировать/удалять аккаунты пользователей;
    - редактировать/удалять любые рецепты;
    - добавлять/удалять/редактировать ингредиенты;
    - добавлять/удалять/редактировать теги.

# Админка
В интерфейс админ-зоны выведены следующие поля моделей и фильтры:
### Модели:
    Доступны все модели с возможностью редактирования и удаления записей.

### Модель пользователей:
    Фильтр по email и имени пользователя.

### Модель рецептов:
    В списке рецептов доступны название и авторы рецептов.
    Фильтры по автору, названию рецепта, тегам.
    Выведена информация о популярности рецепта: общее число добавлений этого рецепта в избранное пользователей.

### Модель ингредиентов:
    В списке ингредиентов доступны название ингредиента и единицы измерения.
    Фильтр по названию.

# Ресурсы сервиса

### Рецепт
Рецепт описывается полями:

    Автор публикации (пользователь).
    Название рецепта.
    Картинка рецепта.
    Текстовое описание.
    Ингредиенты: продукты для приготовления блюда по рецепту с указанием количества и единиц измерения.
    Тег.
    Время приготовления в минутах.

### Тег
Тег описывается полями:

    Название.
    Цветовой HEX-код.
    Slug.

### Ингредиент
Ингредиент описывается полями:

    Название.
    Количество (только для рецепта).
    Единицы измерения.

### Список покупок.
Список покупок скачивается в текстовом формате: shopping-list.txt.

## Фильтрация по тегам
При нажатии на название тега выводится список рецептов, отмеченных этим тегом. Фильтрация может проводится по нескольким тегам в комбинации «или»: если выбраны несколько тегов — в результате должны быть показаны рецепты, которые отмечены хотя бы одним из этих тегов.
При фильтрации на странице пользователя фильтруются только рецепты выбранного пользователя. Такой же принцип соблюдается при фильтрации списка избранного.

# Примеры запросов к API.

Запросы к API начинаются с «/api/v1/»

1) регистрация пользователя

POST-запрос: /api/users/
<br /> *Request sample:*
```python
{

    "email": "string",
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "password": "string"

}
```
*Response sample (201):*
```python
{

    "email": "string",
    "id": 0,
    "username": "string",
    "first_name": "string",
    "last_name": "string"

}
```
*Response sample (400):*
```python
{
    «field_name»: [
      «Обязательное поле.»
    ]
}
```

2) Получение токена

POST-запрос: /api/auth/token/login/
<br /> *Request sample:*
```python
{
    «email»: «string»,
    «password»: «string»
}
```
*Response sample (201):*
```python
{
    «token»: «string»
}
```
*Response sample (400):*
```python
{
    «field_name»: [
      «string»
    ]
}
```
Увидеть полную спецификацию API вы сможете развернув проект локально http://127.0.0.1/api/docs/ или на вашем хосте.

### <br /> Автор проекта:
Алексей Андреев<br />
xost.andreev@yandex.ru<br />
Telegram: @xostyara


Проверка деплой
