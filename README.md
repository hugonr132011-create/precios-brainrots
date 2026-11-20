# precios-brainrots

`prices.json` = precio en **USD** del brainrot más barato que hay a la venta en eldorado.gg, por nombre.
GitHub Actions lo actualiza solo cada 3 horas (`.github/workflows/update.yml`).

## Montarlo (una vez)
1. En GitHub: **New repository** → nombre `precios-brainrots` → **Public** (el hub lo lee sin token) → Create.
2. Sube estos archivos (botón *uploading an existing file*, o `git push`): `update_prices.py`, `prices.json`,
   `README.md` y la carpeta `.github/workflows/update.yml` (la carpeta `.github` tiene que ir tal cual).
3. En el repo: **Settings → Actions → General → Workflow permissions → Read and write permissions** → Save.
4. Pestaña **Actions** → "Actualizar precios" → **Run workflow** para probarlo. Después corre solo.

## En shadow mog
La URL que lee el hub es
`https://raw.githubusercontent.com/hugonr132011-create/precios-brainrots/main/prices.json`.
Cámbiala en `shadow mog.lua` (busca `TU_USUARIO`) o pon antes del script
`getgenv().ShadowPricesUrl = '...'`.

- Tus valores de *Brainrot Values* siguen mandando sobre estos.
- Por defecto solo se actualizan los brainrots que ya tenían valor; `getgenv().ShadowLivePricesAll = true` usa todos.
- `getgenv().ShadowLivePrices = false` lo apaga.

## Notas
- Es la API interna de la web de Eldorado (no oficial): si la cambian, el script deja de sacar precios y
  **no** sobrescribe el `prices.json` bueno (necesita al menos 50 precios).
- EUR→USD con el cambio del BCE (frankfurter.dev).
- Es el precio *más barato* de cada brainrot (normalmente el de menos dinero/s, sin mutación).
