"""Descarga de Eldorado.gg el precio mas barato ("from") de cada brainrot de Steal a Brainrot,
lo pasa de EUR a USD y lo guarda en prices.json. Lo ejecuta GitHub Actions cada pocas horas.

Uso local:  python update_prices.py
"""
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API = "https://www.eldorado.gg/api/v1/item-management/products"
FX = "https://api.frankfurter.dev/v1/latest?base=EUR&symbols=USD"
PAGE_SIZE = 50  # el maximo que acepta la API
OUT = "prices.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (price-tracker)", "Accept": "application/json"}


def get_json(url, tries=4):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # red / 429 / 5xx: reintenta con espera
            last = e
            time.sleep(2 + i * 3)
    raise RuntimeError(f"{url}: {last}")


def eur_to_usd():
    data = get_json(FX)
    return float(data["rates"]["USD"])


def fetch_products():
    items, page, total = [], 1, None
    while True:
        q = urllib.parse.urlencode({
            "gameId": 259, "category": "CustomItem", "pageIndex": page,
            "pageSize": PAGE_SIZE, "useOfferAttributeSearch": "true",
        })
        data = get_json(f"{API}?{q}")
        total = data.get("totalPages") or 1
        items.extend(data.get("results") or [])
        if page >= total:
            break
        page += 1
        time.sleep(1)  # sin prisas para no molestar a la web
    return items


def main():
    rate = eur_to_usd()
    products = fetch_products()
    prices = {}
    for p in products:
        name = (p.get("name") or "").strip()
        fp = p.get("fromPrice") or {}
        amount = fp.get("amount")
        cur = (fp.get("currency") or "EUR").upper()
        if not name or not isinstance(amount, (int, float)) or amount <= 0:
            continue
        usd = amount * rate if cur == "EUR" else amount if cur == "USD" else None
        if usd is None:
            continue
        usd = round(usd, 2)
        # si un nombre sale varias veces nos quedamos con el mas barato
        if name not in prices or usd < prices[name]:
            prices[name] = usd
    if len(prices) < 50:
        # algo ha ido mal (web cambiada / bloqueo): no machacar el archivo bueno
        print(f"solo {len(prices)} precios, no se guarda", file=sys.stderr)
        return 1
    out = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "currency": "USD",
        "eur_usd": rate,
        "source": "eldorado.gg (precio mas barato de cada brainrot)",
        "count": len(prices),
        "prices": dict(sorted(prices.items())),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"{len(prices)} precios guardados en {OUT} (1 EUR = {rate} USD)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
