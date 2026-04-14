async function checkServerStatus() {
    const statusElement = document.getElementById("status-line");
    try {
        const response = await fetch(`http://${SERVER_IP}/status`);
        const data = await response.json();

        if (data.status === "online" || data.system === "sloth") {
            console.log("Sloth is awake!🦥");
            if (statusElement) {
                statusElement.innerText = "SRV: ONLINE";
                statusElement.style.color = "#00ff00"; // Робимо зеленим, коли онлайн
            }
        }
    } catch(error) {
        console.log("Sloth is sleeping...");
        if (statusElement) {
            statusElement.innerText = "SRV: OFFLINE";
            statusElement.style.color = "#555";
        }
    }
}
window.onload = () => {
    checkServerStatus();
// Оновлення годинника
    function updateClock() {
        const now = new Date();
       const h = String(now.getHours()).padStart(2, '0');
       const m = String(now.getMinutes()).padStart(2, '0');
       const s = String(now.getSeconds()).padStart(2, '0');
       const clockElement = document.getElementById('clock');
       if (clockElement) {
           clockElement.innerText = `${h}:${m}:${s}`;
       }
    }

// Реєстрація Service Worker
    if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
            navigator.serviceWorker.register('sw.js')
               .then(reg => console.log('SW Registered!', reg))
               .catch(err => console.log('SW Failed!', err));
       });
    }

// Запуск годинника
    setInterval(updateClock, 1000);
    updateClock();

// --- BATTERY LOGIC ---
    function updateBattery() {
        if ('getBattery' in navigator) {
            navigator.getBattery().then(battery => {
               const update = () => {
                   const level = Math.floor(battery.level * 100);
                   const charging = battery.charging ? "⚡" : "";
                   document.getElementById('battery-status').innerText = `BATT: ${level}% ${charging}`;
               };
               update();
               battery.addEventListener('levelchange', update);
               battery.addEventListener('chargingchange', update);
           });
       }
    }

// --- WEATHER LOGIC (wttr.in) ---
    async function updateWeather() {
        try {
           // Запитуємо погоду в форматі "температура + опис" однією строкою
           const response = await fetch('https://wttr.in/?format=%t+%C');
           const data = await response.text();
           document.getElementById('weather-status').innerText = `WX: ${data.toUpperCase()}`;
       } catch (err) {
           document.getElementById('weather-status').innerText = `WX: OFFLINE`;
       }
    }

// Запускаємо все при завантаженні
    updateBattery();
    updateWeather();
// Оновлюємо погоду кожні 15 хвилин
    setInterval(updateWeather, 900000);
}

const SERVER_IP = "192.168.137.110:8000"; // IP

async function updateStorageStats() {
    try {
        const response = await fetch(`http://${SERVER_IP}/system/storage`);
        const data = await response.json();

        // Оновлюємо текст
        document.getElementById('total-val').innerText = data.total;
        document.getElementById('free-val').innerText = data.free;
        document.getElementById('percent-val').innerText = data.percent;

        // Малюємо прогрес-бар
        const barSize = 10; // кількість символів у смузі
        const filledSize = Math.round((data.percent / 100) * barSize);
        const barText = "#".repeat(filledSize) + "-".repeat(barSize - filledSize);
        document.getElementById('progress-bar').innerText = barText;

    } catch (error) {
        console.error("Помилка зв'язку зі сховищем:", error);
    }
}

// Оновлювати кожні 10 секунд
setInterval(updateStorageStats, 10000);
// Перший запуск відразу
updateStorageStats();