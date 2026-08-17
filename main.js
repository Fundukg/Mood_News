let currentMood = "neutral";
let newsData = [];

// Загрузка базы данных
fetch("news_data.json")
  .then((res) => res.json())
  .then((data) => {
    newsData = data;
    renderGrid();
  });

function changeMood(mood) {
  currentMood = mood;
  document.body.className = mood !== "neutral" ? mood : "";

  document
    .querySelectorAll(".controls button")
    .forEach((b) => b.classList.remove("active-btn"));
  document.getElementById(`btn-${mood}`).classList.add("active-btn");

  renderGrid();
}

function renderGrid() {
  const grid = document.getElementById("news-grid");
  grid.innerHTML = "";

  newsData.forEach((news, index) => {
    const text = news.moods[currentMood];
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
                    <div class="date">${new Date(news.published).toLocaleDateString()}</div>
                    <h3>${news.title}</h3>
                    <p>${text.substring(0, 150)}...</p>
                    <a href="${news.link}" target="_blank" class="source-link" onclick="event.stopPropagation()">Читать источник ↗</a>
                `;
    // По клику открываем сравнение
    card.onclick = () => openModal(index);
    grid.appendChild(card);
  });
}

function openModal(index) {
  const news = newsData[index];
  document.getElementById("modal-original").innerText = news.original_text;
  document.getElementById("modal-rewritten").innerText =
    news.moods[currentMood];
  document.getElementById("modal-mood-title").innerText =
    `Версия: ${currentMood === "neutral" ? "Оригинал" : currentMood === "optimistic" ? "Радостная" : currentMood === "sad" ? "Грустная" : "Ироничная"}`;
  document.getElementById("modal").style.display = "flex";
}

function closeModal(e) {
  document.getElementById("modal").style.display = "none";
}
