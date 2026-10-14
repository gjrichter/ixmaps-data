# sisma-2016-cratere

Geodata for the 2016 central Italy earthquake crater ("cratere sismico").

| File | Content |
|---|---|
| `cratere_sisma_2016.geojson` | 138 comuni of the crater (DL 189/2016, annexes 1, 2, 2-bis); props `name`, `istat`, `prov`, `region` |
| `cratere_sisma_2016.topojson` | same, simplified (15%) |
| `cratere_sisma_2016_outline.geojson` | the 138 comuni dissolved into one outline |
| `cratere_sisma_2016_regions.geojson` | Abruzzo, Lazio, Marche, Umbria outlines (simplified) |
| `cratere_sisma_2016_salaria.geojson` | SS4 Via Salaria, Rome to Porto d'Ascoli (SS4 + RA11 + SP227 stub), one MultiLineString |

## Sources
- Comune list: Commissario straordinario ricostruzione sisma 2016, table "Elenco Comuni RCR" (column "cratere"), https://sisma2016.gov.it/wp-content/uploads/2021/11/Elenco-Comuni_RCR_MV_Danno_01.pdf
- Boundaries: ISTAT 2021 via https://github.com/mlocati/geojson-italy (CC-BY)
- Salaria: © OpenStreetMap contributors (ODbL), extracted via Overpass 2026-10-14

CDN: https://cdn.jsdelivr.net/gh/gjrichter/ixmaps-data@main/by-project/sisma-2016-cratere/
