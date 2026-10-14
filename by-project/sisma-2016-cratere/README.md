# sisma-2016-cratere

Geodata for the 2016 central Italy earthquake crater ("cratere sismico").

| File | Content |
|---|---|
| `cratere_sisma_2016.geojson` | 138 comuni of the crater (DL 189/2016, annexes 1, 2, 2-bis); props `name`, `istat`, `prov`, `region` |
| `cratere_sisma_2016.topojson` | same, simplified (15%) |
| `cratere_sisma_2016_outline.geojson` | the 138 comuni dissolved into one outline |
| `cratere_sisma_2016_regions.geojson` | Abruzzo, Lazio, Marche, Umbria outlines (simplified) |
| `cratere_sisma_2016_salaria.geojson` | SS4 Via Salaria, Rome to Porto d'Ascoli (SS4 + RA11 + SP227 stub), one MultiLineString |
| `sisma_social_infrastructure.geojson` | 730 social-infrastructure points (schools, health, care, community) inside the 138 comuni; props `name`, `tipo`, `amenity`, `group` (education/health/care/community), `comune`, `prov`, `region`, `istat`, `osm_id` |

## Sources
- Comune list: Commissario straordinario ricostruzione sisma 2016, table "Elenco Comuni RCR" (column "cratere"), https://sisma2016.gov.it/wp-content/uploads/2021/11/Elenco-Comuni_RCR_MV_Danno_01.pdf
- Boundaries: ISTAT 2021 via https://github.com/mlocati/geojson-italy (CC-BY)
- Salaria and social-infrastructure points: © OpenStreetMap contributors (ODbL), extracted via Overpass 2026-10-14 (amenity=school|kindergarten|childcare|college|university|hospital|clinic|doctors|pharmacy|nursing_home|social_facility|community_centre|social_centre|library), clipped to the crater comuni

CDN: https://cdn.jsdelivr.net/gh/gjrichter/ixmaps-data@main/by-project/sisma-2016-cratere/
