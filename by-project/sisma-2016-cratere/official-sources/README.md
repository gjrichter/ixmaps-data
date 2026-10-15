# Sisma 2016 cratere: social infrastructure from official sources

All files are limited to the 138 comuni of the crater (DL 189/2016; boundaries in
`cratere_sisma_2016.geojson`, joined by 6-digit ISTAT code `istat`).
Built 2026-10-15. Per-comune summary: `sisma_infrastrutture_per_comune.csv`.

| File | Rows | Source | Notes |
|---|---|---|---|
| `mim_edifici_scolastici_2024_25.csv` | 564 buildings | MIM Anagrafe edilizia scolastica, `EDIANAGRAFESTA202120242520250806.csv` (a.s. 2024/25) | address only, **no coordinates**; deduplicated by `CODICEEDIFICIO` |
| `mim_scuole_statali_2026_27.csv` | 760 | MIM `SCUANAGRAFESTAT20262720260901.csv` | no coordinates; joined by cadastral comune code |
| `mim_scuole_paritarie_2026_27.csv` | 34 | MIM `SCUANAGRAFEPAR20262720260901.csv` | no coordinates |
| `salute_farmacie_attive.csv/.geojson` | 250 (235 with coordinates) | Ministero della Salute, `FRM_FARMA_5_20261013.csv` | active only (no end date); coordinates are partly OSM-derived, verify before precise use |
| `salute_ospedali_posti_letto.csv` | 7 structures | Ministero della Salute, posti letto per struttura (dataset 18), latest year **2019** | no coordinates; bed counts summed over disciplines |
| `salute_consultori_2019.csv` | 31 | Ministero della Salute, consultori familiari (dataset 70), **2019** | no coordinates |
| `sisma_opere_pubbliche_2023_04.csv` | 2673 works, ~3.15 bn EUR programmed | Commissario sisma 2016, Allegato 3 "Database delle opere pubbliche ad Aprile 2023" (PDF, 162 pages) | parsed from PDF positions; status as of 30 Apr 2023 |

## ISTAT files (folder `istat/`, added 2026-10-15)

| File | Rows | ISTAT dataflow | Notes |
|---|---|---|---|
| `istat_nidi_comuni_2024.csv` | 138 comuni | `47_850` Servizi socio-educativi per la prima infanzia (2024) | authorized places (public / private / total), places per 100 children 0-2, services, municipal spending; 58 comuni have places, 3,540 places in total |
| `istat_servizi_sociali_comuni_2022.csv` | 138 | bulk `DF_BULK_DCIS_SPESESERSOC1` (Interventi e servizi sociali dei comuni), 2022 | total spending and per-capita, plus spending by beneficiary group (FAM families/minors, DIS disability, ELD elderly, POV poverty, ADD addictions, IMMNOM immigrants/nomads, MULBEN multi-target); about 83.6 M EUR |
| `istat_servizi_sociali_comuni_serie_2013_2022.csv` | 138 | same | total spending by year |
| `istat_ospedali_posti_letto_comuni.csv` | 6 comuni | `43_994_DF_DCIS_OSPED_COM_2` (Istituti di cura - comuni), 2023 | inpatient and day-hospital beds, all specialties |
| `istat_musei_comuni.csv` | 81 comuni | `60_1004_DF_DCIS_MUSVIS_COM_1` (Musei - comuni) | institutes and visitors; latest year per comune (mostly 2020, some 2011-2019) |

`sisma_infrastrutture_per_comune.csv` also carries six `istat_*` columns taken from these files.

Not available at comune level in the ISTAT warehouse: residential care facilities (`49_37`, regional only), schools (`52_1044`, no comune data for Amatrice at least), social-services dataflow `47_940` via SDMX (times out; the bulk ZIP was used instead).
Available but not extracted: census non-profit institutions by comune (`DF_BULK_CEN2011_DICA_*COM`, 2011/2015), hospital data for more years.

## Caveats
- MIM and health files carry addresses and comune codes but no latitude/longitude; they give per-comune counts, or can be geocoded later.
- Health facility lists are old (2019) except pharmacies.
- The public-works database is a PDF snapshot of April 2023. Wrapped cells were reassembled by position; 64 rows whose comune name was split across lines were matched by name or implementing body. Spot-check before quoting numbers. The programme also includes works in comuni outside the 138 (about 540 rows, not included).
- Not checked: OpenCUP, the GE.DI.SI. contribution table, and regional registries.
