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