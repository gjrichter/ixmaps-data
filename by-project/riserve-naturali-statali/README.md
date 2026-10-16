# riserve-naturali-statali

Two GeoJSON files from the same source: `riserve_naturali_statali.geojson` (147 reserves, `tipo = RNS`) and
`parchi_nazionali.geojson` (24 national parks, `tipo = PNZ`; the list in force has no marine national parks and
predates the newest parks).

The 147 Italian state nature reserves (Riserve Naturali Statali, `tipo = RNS`) from the official list of
protected areas (EUAP), as a GeoJSON file in WGS84 (`riserve_naturali_statali.geojson`, MultiPolygon).

- Source: Ministero dell'Ambiente e della Sicurezza Energetica (MASE), Geoportale Nazionale, service
  "VI Elenco ufficiale aree protette (EUAP)", WFS `http://wms.pcn.minambiente.it/ogc?map=/ms_ogc/wfs/EUAP.map`,
  layer `SP.SITIPROTETTI.EUAP`, filtered `tipo = RNS`. Retrieved 2026-10-16. The service describes the list as the
  VI aggiornamento (D.M. 27/04/2010); a newer decree was reported as being published in July 2026.
- Conversion: GML 3.1.1 to GeoJSON with GDAL, 5 decimals; the WFS 1.1 axis order (lat, lon) was swapped to lon, lat.
- Properties: `name` (nome_gazze), `type` (RNS), `code` (EUAP code), `manager` (ente_gesto), `decree`
  (provvedime), `area_ha`, `naz_reg`.
