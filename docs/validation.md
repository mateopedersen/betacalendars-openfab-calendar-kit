# Validation record

- Gregorian leap-year rule: 1900 no, 2000 yes, 2024 yes, 2027 no, 2100 no, 2400 yes.
- All 12 months of 2027 are generated from Python's Gregorian calendar implementation.
- The generator supports years 1900–2100 and uses six fixed rows for monthly outputs.
- SVG files are XML parsed during generation.
- PDF artifacts are one page each and generated at exact A4 or US Letter page dimensions.
- DXF is ASCII R12-style, millimeter units, with the stencil perimeter as a closed polyline and grid geometry on a separate layer.

Digital validation is not a physical-machine test. Import behavior varies by CAD/CAM software and should be checked locally.
- 104 PDFs are present: 96 monthly combinations (12 months × 2 week starts × 2 paper sizes × 2 orientations) plus 8 undated grid combinations.
- Representative A4/Letter PDFs open as one page and report the expected portrait/landscape page boxes.
