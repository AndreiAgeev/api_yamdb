# API YaMDB
## Описание:
Проект API YaMDB, сделанный в рамках обучения на платформе Yandex.Practicum.
Проект YaMDb собирает отзывы пользователей на произведения (аналог IMDB). Сами произведения в YaMDb не хранятся. Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка», и жанры (присваивается из списка предустановленных).<br />
Проект представляет собой API, написанный с помощью Django Rest Framework. В его функционал входят:
1) Аутентификация пользователей по токену. При регистрации пользователю отправляется письмо с кодом подтверждения на почту, которую пользователь указал. Для получения токена пользователь должен отправить запрос, содержащий данный код;
2) Аутентифицированные пользователи могут писать отзывы на произведения, а также комментировать отзывы других пользователей;
3) Имеется система модерации. На платформе имеются пользователи с правами модераторов и администраторов. Модерация может взаимодействовать с отзывами и комментариями пользователей, если посчитает, что они нарушают правила. Администраторы, помимо этого, также могут добавлять новые произведения, жанры и категории, обновляя базу данных. Администраторы также могут, при необходимости взаимодействовать с данными пользователей;
4) Незарегистрированные пользователи также имеют доступ к платформе, но ограничены только возможностью просмотра контена;
5) Отзывы выражаются не только в текстовом представлении - пользователи вместе с отзывом также выставляют произведению оценку (от 0 до 10), которая затем учитывается в рейтинге произведения.
<br />
Полная документация по API доступна по ссылке http://127.0.0.1:8000/redoc/ после запуска проекта.

## Как запустить проект на локальной машине:
Клонировать репозиторий и перейти в него:
```
git clone https://github.com/AndreiAgeev/api_yamdb.git
```
```
cd api_yamdb/
```
Создать и активировать вирутальное окружение:<br />
*Для Linux:*
```
python3 -m venv env
source env/bin/activate
```
*Для Windows:*
```
python3 -m venv env
source env/Scripts/activate
```
Установить зависимости из файла requirements.txt:<br />
*Для Linux:*
```
python3 -m pip install --upgrade pip
```
*Для Windows:*
```
python -m pip install --upgrade pip
```
Выполнить миграции и запустить проект:<br />
*Для Linux:*
```
python3 manage.py migrate
```
```
python3 manage.py runserver
```
*Для Windows:*
```
python manage.py migrate
```
```
python manage.py runserver
```
