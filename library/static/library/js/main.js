document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("genre-input");
    const genreList = document.getElementById("genre-list");

    // показать/скрыть список
    input.addEventListener("focus", () => {
        genreList.style.display = "block";
    });

    // фильтрация жанров по вводу
    input.addEventListener("input", () => {
        const filter = input.value.toLowerCase();
        genreList.querySelectorAll("li").forEach(li => {
            li.style.display = li.textContent.toLowerCase().includes(filter) ? "block" : "none";
        });
    });

    // выбор жанра
    genreList.querySelectorAll("li").forEach(li => {
        li.addEventListener("click", () => {
            input.value = li.textContent;
            genreList.style.display = "none";
        });
    });

    // скрывать список при клике вне
    document.addEventListener("click", (e) => {
        if (!input.contains(e.target) && !genreList.contains(e.target)) {
            genreList.style.display = "none";
        }
    });
});


