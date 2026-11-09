#!/usr/bin/env python3
"""
Короткие адреса сборок: tshopkz.kz/1041 → страница /1041/index.html,
которая отдаёт превью (фото, название) для WhatsApp/Instagram и сразу
переводит на карточку /#1041.

Запуск из корня репозитория:  python3 tools/gen_pages.py
Берёт данные из prices.json, ничего руками править не нужно.
Безопасно запускать сколько угодно раз (перезаписывает только свои папки).
Цену в превью не пишем специально — она меняется, а превью кэшируется.
"""
import json
import os
import re
import sys
import html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://tshopkz.kz"


def short(s: str) -> str:
    s = re.sub(r"^Ryzen (\d) ", r"R\1 ", s or "")
    return re.sub(r" \d+GB$", "", s)


def main() -> int:
    with open(os.path.join(ROOT, "prices.json"), encoding="utf-8") as f:
        data = json.load(f)
    made = 0
    for b in data.get("builds", []):
        n = b.get("number")
        if not n:
            continue
        n = str(n)
        if not re.fullmatch(r"\d{3,4}", n):
            continue
        img = f"img/{n}.jpg"
        has_img = os.path.exists(os.path.join(ROOT, img))
        name = f"{short(b.get('cpu', ''))} · {short(b.get('gpu', ''))}"
        kind = "Комплект" if b.get("type") == "kit" else "Сборка"
        title = f"{kind} №{n} — {name} · TSHOP"
        if b.get("type") == "kit":
            desc = "Системный блок + монитор и девайсы. Цена на сегодня, замена деталей, рассрочка Kaspi 0-0-24. TSHOP, Астана."
        else:
            desc = "Цена на сегодня, замена деталей в два касания, рассрочка Kaspi 0-0-24, гарантия 1 год. TSHOP, Астана."
        og_img = f"{SITE}/{img}" if has_img else f"{SITE}/img/og.jpg"
        page = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{SITE}/#{n}">
<meta property="og:type" content="product">
<meta property="og:site_name" content="TSHOP.KZ">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{SITE}/{n}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{og_img}">
<link rel="icon" href="/favicon.ico" sizes="any">
<meta name="theme-color" content="#d6202b">
<script>location.replace("/"+(location.search||"")+"#{n}");</script>
<meta http-equiv="refresh" content="0;url=/#{n}">
<style>body{{font-family:system-ui,sans-serif;background:#121316;color:#eee;display:grid;place-items:center;min-height:100vh;margin:0}}a{{color:#fff}}</style>
</head>
<body><p>{html.escape(kind)} №{n} — <a href="/#{n}">открыть на tshopkz.kz</a></p></body>
</html>
"""
        d = os.path.join(ROOT, n)
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, "index.html")
        old = None
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                old = f.read()
        if old != page:
            with open(path, "w", encoding="utf-8") as f:
                f.write(page)
            made += 1
    print(f"страниц обновлено: {made}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
