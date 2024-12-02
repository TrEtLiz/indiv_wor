document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    const header = document.body.querySelector(".header");

    // Установка начальной темы
    const currentTheme = localStorage.getItem('theme') || 'light-theme';
    body.className = currentTheme;

    if (currentTheme === 'dark-theme') {
        themeToggle.textContent = 'Switch to Light Theme';
    } else {
        themeToggle.textContent = 'Switch to Dark Theme';
    }

    themeToggle.addEventListener('click', () => {
        if (body.classList.contains('dark-theme')) {
            body.classList.remove('dark-theme');
            body.classList.add('light-theme');
            header.classList.remove('bg-dark');
            header.classList.add('bg-light');
            localStorage.setItem('theme', 'light-theme');
            themeToggle.textContent = 'Switch to Dark Theme';
        } else {
            body.classList.remove('light-theme');
            body.classList.add('dark-theme');
            header.classList.remove('bg-light');
            header.classList.add('bg-dark');
            localStorage.setItem('theme', 'dark-theme');
            themeToggle.textContent = 'Switch to Light Theme';
        }
    });

    // Смена изображений каждые 30 секунд
    const images = [
        "/static/blog/v_1.jpg",
        "/static/blog/v_2.jpg",
        "/static/blog/v_3.jpg",
        "/static/blog/v_4.jpg",
        "/static/blog/v_5.jpg",
        "/static/blog/v_6.jpg",
        "/static/blog/v_7.jpg",
        "/static/blog/v_8.jpg",
        "/static/blog/v_9.jpg",
        "/static/blog/v_10.jpg",
    ];
    let currentImageIndex = 0;
    const rotatingImage = document.getElementById('rotating-image');

    setInterval(() => {
        currentImageIndex = (currentImageIndex + 1) % images.length;
        rotatingImage.src = images[currentImageIndex];
    }, 10000); // 10 секунд
});
