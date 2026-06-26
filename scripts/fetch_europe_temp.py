#!/usr/bin/env python3
"""Fetch 0.5-degree Europe temperature grid from Open-Meteo and save to JSON."""
import json
import time
import requests
from datetime import datetime, timezone
from pathlib import Path

SPACING   = 0.5
LAT_RANGE = (36, 69)
LON_RANGE = (-12, 33)
CHUNK     = 300
DELAY     = 7.0   # seconds between batches (~8 req/min < Open-Meteo free-tier limit)
MAX_RETRY = 3     # retries per chunk on 429

def build_grid():
    pts, f = [], int(round(1 / SPACING))
    for la in range(int(LAT_RANGE[0] * f), int(LAT_RANGE[1] * f) + 1):
        for lo in range(int(LON_RANGE[0] * f), int(LON_RANGE[1] * f) + 1):
            pts.append((la / f, lo / f))
    return pts

def fetch_chunk(sl):
    lats = ','.join(str(p[0]) for p in sl)
    lons = ','.join(str(p[1]) for p in sl)
    url  = (
        'https://api.open-meteo.com/v1/forecast'
        f'?latitude={lats}&longitude={lons}'
        '&hourly=soil_temperature_0cm,temperature_2m'
        '&forecast_days=1&timezone=UTC'
    )
    for attempt in range(MAX_RETRY):
        resp = requests.get(url, timeout=30)
        if resp.status_code == 429:
            wait = 65 * (attempt + 1)
            print(f'  429 rate-limit — waiting {wait}s (attempt {attempt+1}/{MAX_RETRY})')
            time.sleep(wait)
            continue
        resp.raise_for_status()
        raw = resp.json()
        if not isinstance(raw, list):
            if raw.get('error'):
                raise RuntimeError(raw.get('reason', 'Open-Meteo error'))
            raw = [raw]
        return raw
    raise RuntimeError('Rate-limit persists after retries')

def fetch_all(pts):
    hour  = datetime.now(timezone.utc).hour
    out   = []
    total = len(pts)
    for i in range(0, total, CHUNK):
        sl  = pts[i:i + CHUNK]
        raw = fetch_chunk(sl)
        for j, d in enumerate(raw):
            h = d.get('hourly', {})
            out.append({
                'lat':  sl[j][0],
                'lon':  sl[j][1],
                'soil': (h.get('soil_temperature_0cm') or [None])[hour],
                'air':  (h.get('temperature_2m')        or [None])[hour],
            })
        done = min(i + CHUNK, total)
        print(f'  {done}/{total} pts fetched')
        if done < total:
            time.sleep(DELAY)
    return out, hour

def main():
    pts = build_grid()
    print(f'Grid: {len(pts)} points at {SPACING}deg spacing')
    data, hour = fetch_all(pts)
    out_path = Path(__file__).parent.parent / 'by-project' / 'europe-temperature' / 'grid.json'
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        'updated':   datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'hour_utc':  hour,
        'points':    len(data),
        'data':      data
    }
    out_path.write_text(json.dumps(payload, separators=(',', ':')))
    print(f'Written {len(data)} pts -> {out_path}')

if __name__ == '__main__':
    main()
