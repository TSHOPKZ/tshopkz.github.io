# Сайт TSHOP (tshopkz.kz) — читать перед правкой

Полная карта проекта и правила — в репозитории бота: `TSHOPKZ/tshop-bot`, файл `CLAUDE.md`.

Коротко:
- Пуш в `main` = сайт меняется сразу (GitHub Pages), проверки перед выкладкой нет. Поэтому перед пушем из папки бота:
  `python checks.py --site <эта папка>` — проверит JavaScript в `index.html` и формат `prices.json`.
- `prices.json`, `ai_catalog.txt`, `img/`, папки `/номер/` пишет бот (`site_export.py`) после каждой синхронизации. Руками не править — перезапишется.
- Поля `prices.json` читают сразу четыре места: `index.html`, `tools/gen_pages.py`, клиентский бот (`shop_data.py`), бот заказов (`orders_core.py`). Переименовал поле — поправь все четыре.
- `ai_rules.txt`, `ai_config.json` — ИИ-помощник сайта (Cloudflare-воркер `tshop-order`). `z/` — веб-панель заказов, `z/api.json` пишет бот. `shop.json` — режим «закрыто», пишет бот.
- Форма заказа шлёт заказ в воркер `tshop-order.al-word-kz.workers.dev` → бот заказов. Меняешь поля формы — проверь, что бот заказов их разбирает (`orders_core.py`).
