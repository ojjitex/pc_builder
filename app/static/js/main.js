document.addEventListener("DOMContentLoaded", () => {
    const wishlist = JSON.parse(localStorage.getItem("wishlist")) || [];

    // Логика для кнопок "В избранное"
    document.querySelectorAll(".wishlist-btn").forEach(button => {
        const productId = button.dataset.id;

        if (wishlist.includes(productId)) {
            button.classList.add("active");
            button.textContent = "❤️ В избранном";
        }

        button.addEventListener("click", () => {
            if (wishlist.includes(productId)) {
                wishlist.splice(wishlist.indexOf(productId), 1);
                button.classList.remove("active");
                button.textContent = "❤️ В избранное";
            } else {
                wishlist.push(productId);
                button.classList.add("active");
                button.textContent = "❤️ В избранном";
            }

            localStorage.setItem("wishlist", JSON.stringify(wishlist));
        });
    });

    // Инициализация Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

    // 1. Логика для сравнения товаров
    const compareList = [];
    document.querySelectorAll(".compare-btn").forEach(button => {
        button.addEventListener("click", () => {
            const productId = button.dataset.id;
            if (!compareList.includes(productId)) {
                compareList.push(productId);
                alert(`Товар с ID ${productId} добавлен в сравнение.`);
            } else {
                alert("Этот товар уже добавлен в сравнение.");
            }
        });
    });

    // 2. Логика прогресс-бара
    const progressBar = document.querySelector(".progress-bar");
    let progress = 0;

    function updateProgress(value) {
        progress += value;
        progressBar.style.width = `${progress}%`;
        progressBar.setAttribute("aria-valuenow", progress);
        progressBar.textContent = `${progress}%`;
    }

    // Пример: Обновление прогресса при выборе компонента
    document.querySelectorAll(".card").forEach(card => {
        card.addEventListener("click", () => {
            updateProgress(25); // Увеличиваем прогресс на 25%
        });
    });

    // 3. Логика для переключения темы
    const themeToggle = document.getElementById("theme-toggle");
    const currentTheme = localStorage.getItem("theme") || "dark";
    document.documentElement.setAttribute("data-theme", currentTheme);

    if (currentTheme === "dark") {
        themeToggle.textContent = "☀️ Светлая тема";
    } else {
        themeToggle.textContent = "🌙 Темная тема";
    }

    themeToggle.addEventListener("click", () => {
        const newTheme = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
        document.documentElement.setAttribute("data-theme", newTheme);
        localStorage.setItem("theme", newTheme);

        if (newTheme === "dark") {
            themeToggle.textContent = "☀️ Светлая тема";
        } else {
            themeToggle.textContent = "🌙 Темная тема";
        }
    });

    // 4. Логика для спиннера и анимации карточек
    const loadingSpinner = document.getElementById("loading-spinner");
    const productsContainer = document.getElementById("products-container");

    // Показываем спиннер при загрузке страницы
    loadingSpinner.style.display = "block";

    // Имитация загрузки данных (замените на реальный запрос к API)
    setTimeout(() => {
        loadingSpinner.style.display = "none"; // Скрываем спиннер
        const cards = productsContainer.querySelectorAll(".card");

        // Плавное появление карточек
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add("visible");
            }, index * 100); // Задержка для каждой карточки
        });
    }, 1000); // Задержка в 1 секунду для имитации загрузки
});