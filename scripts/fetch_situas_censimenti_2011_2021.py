#!/usr/bin/env python3
"""Fetch ISTAT SITUAS comune-code translation tables and save as static JSON.

Used by the ixMaps "Popolazione 2011-2021" census-comparison map
(index_embed_italia_censimenti_compare_procom.html + layer_compare.js) to
realign comune codes between the 2011 and 2021 censuses. Re-run this script
periodically (administrative changes are rare - monthly is plenty) and
publish the updated by-project/censimenti-2011-2021/situas_codes.json; the
map fetches that static file instead of calling SITUAS live from the
browser, since situas-servizi.istat.it is a live government reporting
service (Cache-Control: no-store, no CDN) not meant to be hit by every
visitor of a public map on every pan/zoom - see
censimenti_2011_2021_metodo_di_confronto.md for the full history of why.

Two lookups are produced, matching exactly what layer_compare.js needs:

- comune_translation: report 99, a single already-resolved comune-code
  translation 31/12/2011 -> CENSUS_EPOCH_END, combining province changes
  (AP), fusions (CS) and incorporations (ES). Used by query_data_procom_all()
  at comune level.
- ap_only_translation: report 129 (raw variation events since 1991),
  filtered here to AP-type events up to CENSUS_EPOCH_END only. Used by
  query_data() at census-SECTION level, where fusion-type changes must NOT
  be remapped onto section-ID prefixes (spatially wrong in the majority of
  cases - see the method doc, §7.3).

CENSUS_EPOCH_END must match the vintage of the "2021" procom/sezioni census
data - do NOT extend it to "today": remapping 2011 codes past that point
would desync them from the still-2021-vintage codes on the other side of
the comparison (e.g. the 2026 Sardinia province reorganization must NOT be
applied, since the 2021 census data doesn't reflect it either).

Both maps are pre-normalized to the de-padded PROCOM convention used
throughout layer_compare.js (SITUAS returns zero-padded 6-digit codes like
"002114"; the census CSVs use "2114") - the client does a plain lookup,
no further normalization needed.
"""
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CENSUS_EPOCH_END = "31/12/2021"          # DD/MM/YYYY, for the SITUAS request params
CENSUS_EPOCH_END_ISO = "2021-12-31"      # ISO, for comparing against event dates

REPORT_99_URL = (
    "https://situas-servizi.istat.it/publish/reportspooljson"
    f"?pfun=99&pdatada=31/12/2011&pdataa={CENSUS_EPOCH_END}"
)
REPORT_129_URL = (
    "https://situas-servizi.istat.it/publish/reportspooljson"
    f"?pfun=129&pdata={CENSUS_EPOCH_END}"
)


def denpad(code):
    """SITUAS zero-padded 6-digit code ("002114") -> de-padded ("2114"),
    matching the PROCOM convention used by the census CSVs and the rest of
    layer_compare.js (String(Number(...)) there)."""
    return str(int(code))


def fetch_json(url):
    with urllib.request.urlopen(url, timeout=60) as resp:
        return json.load(resp)


def build_comune_translation():
    data = fetch_json(REPORT_99_URL)
    rows = data.get("resultset", [])
    m = {}
    for row in rows:
        src, dst = row.get("PRO_COM_T_DT_IN"), row.get("PRO_COM_T_DT_FI")
        if src and dst:
            m[denpad(src)] = denpad(dst)
    return m, len(rows)


def build_ap_only_translation():
    data = fetch_json(REPORT_129_URL)
    rows = data.get("resultset", [])
    cutoff = datetime.fromisoformat(CENSUS_EPOCH_END_ISO).replace(tzinfo=timezone.utc)
    m = {}
    ap_total = 0
    for row in rows:
        desc = row.get("DESC_COD_VARIAZIONE") or ""
        if not desc.startswith("AP"):
            continue
        ap_total += 1
        src, dst = row.get("PRO_COM_T"), row.get("PRO_COM_T_REL")
        date_str = row.get("DATA_INIZIO_AMMINISTRATIVA") or ""
        if not (src and dst and date_str):
            continue
        event_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        if event_date <= cutoff:
            m[denpad(src)] = denpad(dst)
    return m, len(rows), ap_total


def main():
    print(f"Fetching report 99 (comune translation) -> {REPORT_99_URL}")
    comune_translation, r99_rows = build_comune_translation()
    print(f"  {r99_rows} rows, {len(comune_translation)} mapped")

    print(f"Fetching report 129 (AP-only translation) -> {REPORT_129_URL}")
    ap_only_translation, r129_rows, ap_total = build_ap_only_translation()
    print(f"  {r129_rows} rows total, {ap_total} AP-type, {len(ap_only_translation)} kept (<= {CENSUS_EPOCH_END_ISO})")

    out_path = Path(__file__).parent.parent / "by-project" / "censimenti-2011-2021" / "situas_codes.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "census_epoch_end": CENSUS_EPOCH_END,
        "sources": {
            "report_99": REPORT_99_URL,
            "report_129": REPORT_129_URL,
        },
        "comune_translation": comune_translation,
        "ap_only_translation": ap_only_translation,
    }
    out_path.write_text(json.dumps(payload, separators=(",", ":")))
    print(f"Written -> {out_path}")


if __name__ == "__main__":
    main()
