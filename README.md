# LiveBar Backend — Render-ready

## Развёртывание (минимум действий)
1) Создай пустой репозиторий на GitHub и **загрузи сюда всё содержимое**.
2) На https://render.com → New → Blueprint → укажи ссылку на репозиторий.
3) Нажми Deploy. Через пару минут получишь URL вида:
   https://livebar-almaty.onrender.com
4) Проверка:
   - GET /api/venues — список заведений
   - GET /api/health — {"ok": true}

## Обновление загруженности
POST /api/venue/neon/reading
Body JSON: { "source":"admin", "value":0.62 }