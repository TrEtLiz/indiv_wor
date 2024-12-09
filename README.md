# ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ МОЛДОВЫ  
**ФАКУЛЬТЕТ МАТЕМАТИКИ И ИНФОРМАТИКИ**  
**ДЕПАРТАМЕНТ ИНФОРМАТИКИ**  

---

### Третьякова Елизавета  

## Индивидуальная работа  
по дисциплине „РАЗРАБОТКА ВЕБ ПРИЛОЖЕНИЙ”  

---

### Руководитель:  
_____________________  
Плешка Наталья, проф. универ.  
(подпись)  

### Автор:  
_____________________  
(подпись)  

---

Кишинёв, 2024

### Содержание

1. [Постановка задачи](#1-постановка-задачи)
2. [Краткое описание Django](#2-краткое-описание-django)
3. [Пошаговое описание создания проекта](#3-пошаговое-описание-создания-проекта)
    - [Шаг 1: Установка Django и создание проекта](#шаг-1-установка-django-и-создание-проекта)
    - [Шаг 2: Создание приложения](#шаг-2-создание-приложения)
    - [Шаг 3: Настройка модели](#шаг-3-настройка-модели)
    - [Шаг 4: Миграции базы данных](#шаг-4-миграции-базы-данных)
    - [Шаг 5: Реализация View и URL](#шаг-5-реализация-view-и-url)
    - [Шаг 6: Настройка шаблонов](#шаг-6-настройка-шаблонов)
    - [Шаг 7: Поиск постов](#шаг-7-поиск-постов)
    - [Шаг 8: Добавление стилей](#шаг-8-добавление-стилей)
4. [Описание файлов проекта](#4-описание-файлов-проекта)

---

#### **1. Постановка задачи**

Разработать веб-приложение на Django, представляющее собой блог, где пользователи могут:

- Создавать и редактировать посты;
- Комментировать публикации;
- Искать посты по заголовкам и содержимому;
- Просматривать список постов и отдельные публикации;
- Ставить лайки постам (опционально).

**Предметная область**: система блогов, которая предоставляет пользователям возможность взаимодействовать с контентом и друг с другом.

---

#### **2. Краткое описание Django**

**Django** — это фреймворк для разработки веб-приложений на Python. Он предоставляет удобный способ построения приложений с использованием архитектурной модели **MVT** (Model-View-Template).

- **Model**: отвечает за работу с базой данных (создание таблиц, запросы).
- **View**: обрабатывает запросы, выполняет бизнес-логику и возвращает результат.
- **Template**: отвечает за отображение данных пользователю (HTML, CSS, JavaScript).

Архитектура MVT помогает разделить логику, представление и данные, упрощая поддержку и тестирование кода.

---

#### **3. Пошаговое описание создания проекта**

##### **Шаг 1: Установка Django и создание проекта**

1. Установите Django:

    ```bash
    pip install django
    ```

2. Создайте новый проект:

    ```bash
    django-admin startproject MyBlog
    ```

3. Перейдите в папку проекта:

    ```bash
    cd MyBlog
    ```

4. Запустите сервер:

    ```bash
    python manage.py runserver
    ```

---

##### **Шаг 2: Создание приложения**

1. Создайте новое приложение:

    ```bash
    python manage.py startapp blog
    ```

2. Зарегистрируйте приложение в `settings.py`:

    ```python
    INSTALLED_APPS = [
         # ...
         'blog.apps.BlogConfig',
    ]
    ```

---

##### **Шаг 3: Настройка модели**

Создайте модели для постов и комментариев в `models.py` приложения `blog`:

```python
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
     title = models.CharField(max_length=250)
     body = models.TextField()
     publish = models.DateTimeField(default=timezone.now)
     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')

     def __str__(self):
          return self.title

class Comment(models.Model):
     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
     body = models.TextField()
     author = models.ForeignKey(User, on_delete=models.CASCADE)
     created = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return f'Комментарий от {self.author} к {self.post}'
```

---

##### **Шаг 4: Миграции базы данных**

1. Создайте миграции:

    ```bash
    python manage.py makemigrations
    ```

2. Примените миграции:

    ```bash
    python manage.py migrate
    ```

---

##### **Шаг 5: Реализация View и URL**

1. В `views.py` добавьте отображение списка постов:

    ```python
    from django.shortcuts import render
    from .models import Post

    def post_list(request):
         posts = Post.objects.all()
         return render(request, 'blog/post_list.html', {'posts': posts})
    ```

2. Настройте маршруты в `urls.py` приложения `blog`:

    ```python
    from django.urls import path
    from . import views

    urlpatterns = [
         path('', views.post_list, name='post_list'),
    ]
    ```

3. В `urls.py` проекта подключите маршруты приложения `blog`:

    ```python
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
         path('admin/', admin.site.urls),
         path('', include('blog.urls')),
    ]
    ```

---

##### **Шаг 6: Настройка шаблонов**

1. Создайте папку `templates/blog`.

2. Добавьте файл `post_list.html`:

    ```html
    {% extends 'base.html' %}

    {% block content %}
    <h1>Список постов</h1>
    <ul>
         {% for post in posts %}
         <li><a href="#">{{ post.title }}</a> - {{ post.publish }}</li>
         {% endfor %}
    </ul>
    {% endblock %}
    ```

3. Создайте файл `base.html` в папке `templates`:

    ```html
    <!DOCTYPE html>
    <html lang="ru">
    <head>
         <meta charset="UTF-8">
         <title>MyBlog</title>
         <link rel="stylesheet" href="{% static 'blog/styles.css' %}">
    </head>
    <body>
         {% block content %}{% endblock %}
    </body>
    </html>
    ```

---

##### **Шаг 7: Поиск постов**

1. Добавьте функцию поиска в `views.py`:

    ```python
    from django.db.models import Q

    def post_search(request):
         query = request.GET.get('q')
         results = []
         if query:
              results = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
         return render(request, 'blog/post_search.html', {'query': query, 'results': results})
    ```

2. Настройте маршрут поиска в `urls.py`:

    ```python
    path('search/', views.post_search, name='post_search'),
    ```

3. В `base.html` добавьте форму поиска:

    ```html
    <form action="{% url 'post_search' %}" method="get">
         <input type="text" name="q" placeholder="Поиск...">
         <button type="submit">Найти</button>
    </form>
    ```

---

##### **Шаг 8: Добавление стилей**

1. В `static/blog/styles.css` добавьте базовые стили:

    ```css
    body {
         font-family: Arial, sans-serif;
         background-color: #f0f0f0;
         margin: 0;
         padding: 0;
    }

    h1 {
         color: #333;
    }

    ul {
         list-style-type: none;
         padding: 0;
    }

    li {
         margin: 10px 0;
    }

    a {
         text-decoration: none;
         color: #0066cc;
    }

    a:hover {
         text-decoration: underline;
    }
    ```

2. Убедитесь, что настройки статических файлов корректны в `settings.py`:

    ```python
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [BASE_DIR / 'static']
    ```

---

#### **4. Описание файлов проекта**

- `blog/static/blog/styles.css`  
  Содержит стили для оформления веб-приложения.

- `blog/templates/blog/base.html`  
  Базовый шаблон приложения.

- `blog/templates/blog/post_list.html`  
  Шаблон для отображения списка постов.

- `blog/views.py`  
  Содержит функции представления для обработки запросов.

- `blog/models.py`  
  Определяет модели данных для постов и комментариев.

- `blog/urls.py`  
  Настраивает URL-маршруты приложения.

- `lab10_djangoproject/settings.py`  
  Файл настроек проекта Django.

- `lab10_djangoproject/urls.py`  
  Главный файл маршрутизации проекта.

- `db.sqlite3`  
  База данных проекта.
