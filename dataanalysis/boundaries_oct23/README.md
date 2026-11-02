# d65_boundaries.html on the Oct 23, 2026 draft

Scripts that moved every tab of `d65_boundaries.html` from the Oct 13 tentative lines to the district's Oct 23 draft.

1. `build_data.py` rebuilds the line-dependent data (land shares, walking distances, middle school zones, Census-based
   shares and walks, kids by area, race by area) from today's and Oct 23 lines (district FY28 Proposed Boundaries map, as placed
   on the D65 School Circles map frame: `M.json`, read from `d65_circles.html`).
2. `tiles.py` computes the area and boundary-line disruption tiles.
3. `assemble.py` swaps the data into the page and updates numbers and text (district Oct 28 counts, our Oct 29 projection,
   LoDN seat rule, new basemap).
4. `integrate.py` adds the "Oct 23 draft" tab group that embeds `d65_circles.html`.

`landdist.py` reproduces the page's earlier Oct 13 land figures exactly from its old polygons (district average walk
0.57 -> 0.68 mi, Dewey shares 28/28/26/18), which is the check on the method. Paths in the scripts point at the build
workspace; adjust `B` in `geo.py` to rerun.
