# Payment

[Тестовое задание](https://docs.google.com/document/d/1X8yV7jAZWZWhy3NG3m_Yi8lW4Bfa6ZNGDx95pHkE_qc/edit#heading=h.qn8kbnfz56hc)

## Технологии

[Django](https://www.djangoproject.com/)

[Stripe](https://stripe.com/)

[PostgeSQL](https://www.postgresql.org/)

## Запуск

Установка на Windows:

1. Склонировать проект с GitHub:
```sh
git clone git@github.com:DarkProrokk/Payment.git
```
2. Перейти в директорию проекта
```sh
cd .\Payment
```
3. Создать виртуальное окружение:

```sh
python -m venv venv
```
4. Активировать виртуальное окружение:
```sh
venv/Scripts/activate - Windows
source env/bin/activate - Linux
```
5. Установить зависимости:
```sh
pip install -r requirements-windows.txt - Windows

pip install -r requirements.txt - Linux
```
6. В файле .env:
    
    * Изменить конфигурацию для подключения к базе данных

    * Добавить api-keys для Stripe

    * Изменить данные для создания superuser(или оставить стандартные)


7. Применить миграции:
```sh
python manage.py migrate
```
8. Создать суперпользователя для доступа к Django admin:
```sh
python manage.py initadmin
```
9. Запустить сервер:
```sh
python manage.py runserver
```
10. Перейти по ссылке:


http://127.0.0.1:8000/
# Запуск при помощи docker-compose:
1. Склонировать проект с GitHub:
```sh
git clone git@github.com:DarkProrokk/Payment.git
```
2. Перейти в директорию проекта
```sh
cd .\Payment
```
3. Изменить в файле .env:
    
    * api-keys для Stripe
    
    * Изменить данные для создания superuser(или оставить стандартные)


4. Создание и запуск контейнера:
```sh
docker compose up
```

5. Перейти по ссылке:

http://127.0.0.1:8000/

Остановка контейнера:
```sh
docker compose stop
```

# Endpoints
Доступ в admin-панель:

`admin/` - При стандартных настройках Login: root | Password: root

Получения информации об Item по его id и оформление заказа с помощью кнопки Buy:
`payment/item/{item_id}/`

Получение session_id для оформления покупки на Stripe:
`payment/buy/{item_id}/`

Покупка всех товаров в Order:
`payment/order_buy/{order_id}/`

# Выполненные дополнительные задачи:
· Запуск используя Docker

· Использование environment variables

· Просмотр Django Моделей в Django Admin панели

· Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей
стоимостью всех Items

· Модели Discount, Tax, которые можно прикрепить к модели Order и связать с соответствующими атрибутами при создании платежа в Stripe в таком случае они корректно отображаются в Stripe Checkout форме.

· Добавить поле Item.currency, создать 2 Stripe Keypair на две разные валюты и в зависимости от валюты выбранного товара предлагать оплату в соответствующей валюте
