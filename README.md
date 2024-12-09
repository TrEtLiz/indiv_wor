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

### Отчёт по индивидуальной работе

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

Архитектура MVT помогает разделить логику, представление и данные, делая код проще для поддержки и тестирования.

---

#### **3. Пошаговое описание создания проекта**

---

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

**Необходим скриншот:** окно консоли с выполнением команды `runserver`.

---

##### **Шаг 2: Создание приложения**
1. Создайте новое приложение:
    ```bash
    python manage.py startapp blog
    ```
2. Зарегистрируйте приложение в `settings.py`:
    ```python
    INSTALLED_APPS = [
        ...
        'blog.apps.BlogConfig',
    ]
    ```

**Необходим скриншот:** изменения в `INSTALLED_APPS` в `settings.py`.

---

##### **Шаг 3: Настройка модели**
Создайте модель для постов и комментариев в `models.py` приложения `blog`:

```python
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
```

**Необходим скриншот:** файл `models.py`.

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

**Необходим скриншот:** вывод команд `makemigrations` и `migrate`.

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
2. Настройте маршрут в `urls.py` приложения `blog`:
    ```python
    from django.urls import path
    from . import views

    urlpatterns = [
        path('', views.post_list, name='post_list'),
    ]
    ```

**Необходим скриншот:** файл `views.py` и `urls.py`.

---

##### **Шаг 6: Настройка шаблонов**
1. Создайте папку `templates/blog` в корне проекта.
2. Добавьте файл `post_list.html`:
    ```html
    {% extends 'base.html' %}
    {% block content %}
    <h1>Список постов</h1>
    <ul>
        {% for post in posts %}
        <li>{{ post.title }} - {{ post.publish }}</li>
        {% endfor %}
    </ul>
    {% endblock %}
    ```

**Необходим скриншот:** файл `post_list.html` и результат в браузере.

---

##### **Шаг 7: Поиск постов**
1. Добавьте функцию поиска в `views.py`:
    ```python
    from django.db.models import Q

    def post_search(request):
        query = request.GET.get('q', '')
        results = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query)) if query else []
        return render(request, 'blog/post_search.html', {'query': query, 'results': results})
    ```
2. Настройте маршрут поиска:
    ```python
    path('search/', views.post_search, name='post_search'),
    ```
3. В `base.html` добавьте строку поиска:
    ```html
    <form action="{% url 'post_search' %}" method="get">
        <input type="text" name="q" placeholder="Поиск...">
        <button type="submit">Найти</button>
    </form>
    ```

**Необходим скриншот:** результат работы строки поиска.

---

##### **Шаг 8: Добавление стилей**
В `static/blog/styles.css` добавьте базовые стили:

```css
body {
    font-family: Arial, sans-serif;
    background-color: #f0f0f0;
}

h1 {
    color: #333;
}
```

Подключите CSS в `base.html`:
```html
<link rel="stylesheet" href="{% static 'blog/styles.css' %}">
```

**Необходим скриншот:** результат со стилями в браузере.

---

Если тебе нужно дополнительно пояснить или переслать файлы, дай знать! 😊
