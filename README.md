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
  ```css
    /* Светлая тема */
    body.light-theme {
        background-color: #bdbdbd;
        color: #000000;
    }

    body.light-theme .navbar {
        background-color: #606060;
        color: #000000;
    }


    body.light-theme a.navbar-brand, body.light-theme a.nav-link, body.light-theme span.nav-link, body.light-theme button.nav-link, body.light-theme .btn {
        color: #030404;
    }

    body.light-theme .card {
        background-color: #dadada; /* Белый фон карточек */
        color: #000000; /* Тёмный текст */
        border: 1px solid #dee2e6; /* Светлая рамка */
    }

    body.light-theme .pagination .page-link {
        background-color: #c8c8c8;
        color: #000000;
        border: 1px solid #dee2e6;
    }

    body.light-theme .pagination .page-link:hover {
        background-color: #bfbfbf; /* При наведении */
        color: #000000;
    }


    /*footer.light-theme {*/
    /*    background-color: #606060;*/
    /*    color: #000000;*/
    /*    padding: 10px 0;*/
    /*}*/

    /* Тёмная тема */
    body.dark-theme {
        background-color: #4e4e4e;
        color: #f8f9fa;
    }

    body.dark-theme .navbar {
        background-color: #212529;
        color: #f8f9fa;
    }


    body.dark-theme a.navbar-brand, body.dark-theme a.nav-link, body.dark-theme span.nav-link {
        color: #f8f9fa;
    }

    body.dark-theme button.nav-link, body.dark-theme .btn {
        background-color: #4e4e4e;
        color: #f8f9fa;
    }

    body.dark-theme .card {
        background-color: #212529; /* Тёмный фон карточек */
        color: #f8f9fa; /* Светлый текст */
        border: 1px solid #495057; /* Тёмная рамка */
    }
    body.dark-theme  {
        color: #f8f9fa;
    }
    body.dark-theme .pagination{
        background-color: #212529;
        color: #f8f9fa;
        border: 1px solid #495057;
    }

    body.dark-theme .pagination .page-link {
        background-color: #343a40;
        color: #f8f9fa;
        border: 1px solid #495057;
    }

    body.dark-theme .pagination .page-link:hover {
        background-color: #343a40; /* При наведении */
        color: #f8f9fa;
    }

    /*footer.dark-theme {*/
    /*    background-color: #212529;*/
    /*    color: #f8f9fa;*/
    /*    padding: 10px 0;*/
    /*}*/

    /* Поисковая форма */
    form.d-flex input[type="search"] {
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 5px 10px;
    }

    form.d-flex button {
        background-color: #6c757d;
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 5px;
        cursor: pointer;
    }

    form.d-flex button:hover {
        background-color: #5a6268;
    }

    /* Для плавной смены изображений */
    #rotating-image {
        transition: opacity 0.5s ease-in-out;
    }

    .image-slider {
        position: relative;
        display: inline-block;
        text-align: center;
    }

    #rotating-image {
        max-width: 100%;
        /*max-height: 60vh;*/
        height: auto;
        display: block;
    }

    .arrow-btn {
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        background-color: rgba(0, 0, 0, 0.5); /* Полупрозрачный фон */
        color: #000000;
        border: none;
        padding: 5px 10px;
        cursor: pointer;
        z-index: 10;
        font-size: 18px;
        border-radius: 50%;
        opacity: 0.8;
        transition: opacity 0.3s;
    }

    .arrow-btn:hover {
        opacity: 1;
    }

    .arrow-btn:focus {
        outline: none;
    }

    .arrow-btn[style*="left"] {
        left: 10px;
    }

    .arrow-btn[style*="right"] {
        right: 10px;
    }
  ```

- `blog/templates/blog/base.html`  
  ```html
    {% load static %}
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{% block title %}My Blog{% endblock %}</title>
        <!-- Подключение CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootswatch@5.3.2/dist/morph/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="{% static 'blog/styles.css' %}">
        <!-- Подключение JS -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" defer></script>
        <script src="{% static 'blog/script.js' %}" defer></script>

    </head>
    <body data-bs-theme="light" class="light-theme">
        <!-- Шапка сайта -->
        <header class="header">
            <nav class="navbar navbar-expand-lg ">
                <div class="container">
                    <a class="navbar-brand" href="/">My Blog</a>
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarNav">
                        <ul class="navbar-nav me-auto">
                            <li class="nav-item">
                                <a class="nav-link" href="/">Главная</a>
                            </li>
                            {% if user.is_authenticated %}
                                <li class="nav-item">
                                    <a class="nav-link" href="{% url 'post_create' %}">Создать пост</a>
                                </li>
                            {% endif %}
                        </ul>
                        <form class="d-flex" action="{% url 'post_search' %}" method="get">
                            <input class="form-control me-2" type="search" name="q" placeholder="Поиск..." aria-label="Search">
                            <button class="btn btn-outline-light" type="submit">Найти</button>
                        </form>

                        <ul class="navbar-nav ms-auto align-items-center">
                            {% if user.is_authenticated %}
                                <li class="nav-item">
                                    <span class="nav-link">Привет, {{ user.username }}!</span>
                                </li>
                                <li class="nav-item">
                                    <form action="{% url 'logout' %}" method="post" style="display:inline;">
                                        {% csrf_token %}
                                        <button type="submit" class="btn btn-link nav-link">Выйти</button>
                                    </form>
                                </li>
                            {% else %}
                                <li class="nav-item">
                                    <a class="nav-link" href="{% url 'login' %}">Вход</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" href="{% url 'register' %}">Регистрация</a>
                                </li>
                            {% endif %}
                            <!-- Кнопка переключения темы -->
                            <li class="nav-item">
                                <button id="theme-toggle" class="btn btn-outline-light ms-2 ">Switch Theme</button>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
        </header>

        
        <!-- Основной контент -->
        <main class="container my-5">
            {% block content %}
            <!-- Контент страниц будет подставлен сюда -->
            {% endblock %}
            <aside class="sidebar">
                {% include 'sidebar_contacts.html' %}
            </aside>

        </main>

        <!-- Футер -->
        <footer class="footer bg-dark text-white py-3">
            <div class="container text-center">
                <p>&copy; 2024 My Blog</p>
            </div>
        </footer>
    </body>
    </html>
    ```

- `blog/templates/blog/post_list.html`  
  ```html
    {% extends 'base.html' %}
    {% load static %}

    {% block title %}Список постов{% endblock %}

    {% block content %}
    <div class="row">
        <!-- Post List -->
        <section class="col-md-8 post-list">
            {% for post in page_obj %}
            <article class="post mb-4 card shadow-sm">
                <div class="card-body">
                    <!-- Заголовок с ссылкой -->
                    <h2 class="card-title">
                        <a href="{% url 'post_detail' post.id %}">{{ post.title }}</a>
                    </h2>
                    <!-- Время публикации -->
                    <p class="card-subtitle text-muted">Опубликовано: {{ post.publish }}</p>
                </div>
            </article>
            {% empty %}
            <p>Нет доступных постов.</p>
            {% endfor %}

            <!-- Пагинация -->
            <div class="pagination">
                <span class="step-links">
                    {% if page_obj.has_previous %}
                        <a href="?page=1">&laquo; Первая</a>
                        <a href="?page={{ page_obj.previous_page_number }}">Предыдущая</a>
                    {% endif %}

                    <span class="current">
                        Страница {{ page_obj.number }} из {{ page_obj.paginator.num_pages }}.
                    </span>

                    {% if page_obj.has_next %}
                        <a href="?page={{ page_obj.next_page_number }}">Следующая</a>
                        <a href="?page={{ page_obj.paginator.num_pages }}">Последняя &raquo;</a>
                    {% endif %}
                </span>
            </div>
        </section>
        <!-- Sidebar -->
        <aside class="col-md-4">
            {% include 'blog/sidebar_images.html' %}
        </aside>
    </div>
    {% endblock %}

    ```
- `blog/views.py`  
  ```python
    from django.shortcuts import render, redirect
    from django.contrib.auth.decorators import login_required
    from .models import Post
    from .forms import UserRegistrationForm, CommentForm, PostForm
    from django.utils.text import slugify
    from django.core.paginator import Paginator

    from django.db.models import Q

    def post_search(request):
        query = request.GET.get('q', '')  # Получаем запрос пользователя из параметра `q`
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        ) if query else []
        return render(request, 'blog/post_search.html', {'query': query, 'results': results})


    def register(request):
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post_list(request):
        posts = Post.objects.all()
        paginator = Paginator(posts, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        comment_form = CommentForm()

        if request.method == 'POST':
            if not request.user.is_authenticated:
                return redirect('login')
            form = CommentForm(request.POST)
            if form.is_valid():
                post_id = request.POST.get('post_id')
                post = Post.objects.get(id=post_id)
                comment = form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
                return redirect('post_list')

        return render(request, 'blog/post_list.html', {'page_obj': page_obj, 'comment_form': comment_form})

    @login_required
    def post_create(request):
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.status = 'published'
                post.slug = slugify(post.title)
                post.save()
                return redirect('post_list')  # Редирект после успешного создания
        else:
            form = PostForm()
        return render(request, 'blog/post_create.html', {'form': form})

    def post_detail(request, post_id):
        post = Post.objects.get(id=post_id)
        comment_form = CommentForm()

        if request.method == 'POST':
            if request.user.is_authenticated:
                form = CommentForm(request.POST)
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.author = request.user
                    comment.post = post
                    comment.save()
                    return redirect('post_detail', post_id=post_id)

        return render(request, 'blog/post_detail.html', {'post': post, 'comment_form': comment_form})
  ```

- `blog/models.py`  
  ```python
    from django.db import models
    from django.utils import timezone
    from django.contrib.auth.models import User

    class Post(models.Model):
        STATUS_CHOICES = (
            ('draft', 'Draft'),
            ('published', 'Published'),
        )
        title = models.CharField(max_length=250)
        slug = models.SlugField(max_length=250, unique_for_date='publish')
        author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
        body = models.TextField()
        publish = models.DateTimeField(default=timezone.now)
        created = models.DateTimeField(auto_now_add=True)
        updated = models.DateTimeField(auto_now=True)
        status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

        class Meta:
            ordering = ('-publish',)

        def __str__(self):
            return self.title

    class Comment(models.Model):
        post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
        author = models.ForeignKey(User, on_delete=models.CASCADE)
        body = models.TextField('Комментарий')
        created = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f'Комментарий от {self.author} к посту {self.post}'
  ```

- `blog/urls.py`  
  ```python
    from django.urls import path
    from . import views

    urlpatterns = [
        path('', views.post_list, name='post_list'),
        path('register/', views.register, name='register'),
        path('create/', views.post_create, name='post_create'),
        path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    ]
  ```

- `lab10_djangoproject/settings.py`  
  ```python
    from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent.parent


    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'django-insecure-zo41na^^-xux+bjd(fgx(_#muef!5co*17@kpkklno98n@4bt#'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = []

    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    # Другие приложения
        'blog.apps.BlogConfig',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'Lab10_DjangoProject.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'templates'],  # Убедитесь, что здесь указан правильный путь
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]


    WSGI_APPLICATION = 'Lab10_DjangoProject.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/5.1/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


    # Password validation
    # https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]


    # Internationalization
    # https://docs.djangoproject.com/en/5.1/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/5.1/howto/static-files/

    STATIC_URL = '/static/'


    # Default primary key field type
    # https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    LOGOUT_REDIRECT_URL = '/'
    LOGIN_REDIRECT_URL = '/'  ```

- `lab10_djangoproject/urls.py`  
  ```python
    from django.contrib import admin
    from django.urls import path, include
    from django.contrib.auth import views as auth_views
    from django.contrib.auth import urls as auth_urls

    from blog import views

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('blog.urls')),
        path('accounts/', include('django.contrib.auth.urls')),  # Это важно
        path('accounts/', include(auth_urls)),
        path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

        path('search/', views.post_search, name='post_search'),
    ]
    ```

- `db.sqlite3`  
    ```markdown
    ### **Пользователи (Users):**
    - **id**: Целое число, первичный ключ, автоинкремент  
    - **username**: Строка, уникальное, обязательное поле  
    - **email**: Строка, уникальное, обязательное поле  
    - **password**: Строка, обязательное поле  
    - **date_joined**: Дата и время, обязательное поле  

    ### **Посты (Posts):**
    - **id**: Целое число, первичный ключ, автоинкремент  
    - **title**: Строка, обязательное поле  
    - **body**: Текст, обязательное поле  
    - **author_id**: Целое число, внешний ключ (ссылается на Users.id), обязательное поле  
    - **slug**: Строка, уникальное, обязательное поле  
    - **status**: Строка, обязательное поле  
    - **created_at**: Дата и время, обязательное поле  
    - **updated_at**: Дата и время, обязательное поле  

    ### **Комментарии (Comments):**
    - **id**: Целое число, первичный ключ, автоинкремент  
    - **body**: Текст, обязательное поле  
    - **author_id**: Целое число, внешний ключ (ссылается на Users.id), обязательное поле  
    - **post_id**: Целое число, внешний ключ (ссылается на Posts.id), обязательное поле  
    - **created_at**: Дата и время, обязательное поле  

    ---

    ## Связи

    ### **Пользователи и Посты (Users to Posts):**  
    - Один пользователь может создать несколько постов.  
    - Каждый пост принадлежит одному пользователю.  

    ### **Пользователи и Комментарии (Users to Comments):**  
    - Один пользователь может написать несколько комментариев.  
    - Каждый комментарий принадлежит одному пользователю.  

    ### **Посты и Комментарии (Posts to Comments):**  
    - Один пост может иметь несколько комментариев.  
    - Каждый комментарий относится к одному посту.  
    ```
