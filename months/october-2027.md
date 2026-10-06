# October 2027 fixture

Generated dated geometry for October 2027, with Monday-first and Sunday-first variants. The monthly fabrication SVGs use a fixed six-row grid for consistent stencil and page geometry.

## Calendar geometry

- Days in month: 31
- First weekday: May (Monday-first index 4)
- Natural week rows: 5 (Monday-first), 6 (Sunday-first)
- Fixed mode: 42 cells, six rows, seven columns; only this month's 31 dates are numbered.

## Generated files

- Plotter SVGs: `fabrication/plotter/2027/october-2027-monday-fixed.svg` and `fabrication/plotter/2027/october-2027-sunday-fixed.svg`. Each has the 7×6 grid, weekday header, 31 date labels and notes region.
- Printable PDFs: eight one-page files in `printable/a4/` and `printable/letter/`: Monday/Sunday start × portrait/landscape.
- The SVG geometry is designed for plotter adaptation; text uses standard fonts and may need conversion to paths for some controllers.

## Validation

The date sequence is generated from Gregorian calendar calculations and included in the 1900–2100 test sweep. SVG XML and printable page dimensions are checked in the project validation. No physical plotter or printer test is claimed.

Human-readable reference: [October calendar](https://www.betacalendars.com/october-calendar.html)
