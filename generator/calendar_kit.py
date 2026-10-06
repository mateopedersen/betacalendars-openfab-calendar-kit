#!/usr/bin/env python3
"""Dependency-free SVG and PDF calendar generator for the OpenFab Calendar Kit."""
import argparse
import calendar
import html
from pathlib import Path

MONTHS = list(calendar.month_name)[1:]
HEADERS = {
    0: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    6: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
}
PAPERS = {'a4': (210.0, 297.0), 'letter': (215.9, 279.4)}

def page_dimensions(paper, orientation):
    w, h = PAPERS[paper]
    return (h, w) if orientation == 'landscape' else (w, h)

def month_grid(year, month, week_start, grid_mode):
    offset = (calendar.monthrange(year, month)[0] - week_start) % 7
    days = calendar.monthrange(year, month)[1]
    natural_rows = (offset + days + 6) // 7
    rows = 6 if grid_mode == 'fixed' else natural_rows
    values = [n - offset + 1 if 1 <= n - offset + 1 <= days else None for n in range(rows * 7)]
    return values, rows

def make_svg(year, month, week_start=0, blank=False, rows=6, paper='a4', orientation='portrait', margin=8.0, notes=True, grid_mode='fixed'):
    width, height = page_dimensions(paper, orientation)
    margin = float(margin)
    note_h = 22.0 if notes else 0.0
    title = 'Undated Calendar' if blank else f'{MONTHS[month-1]} {year}'
    headers = HEADERS[week_start]
    date_rows = rows if blank else (6 if grid_mode == 'fixed' else month_grid(year, month, week_start, 'natural')[1])
    grid_x, grid_y = margin, margin + note_h + 8.0
    grid_w = width - 2 * margin
    header_h = 9.0
    grid_h = height - margin - grid_y - header_h - 30.0
    cell_w, cell_h = grid_w / 7, grid_h / date_rows
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:g}mm" height="{height:g}mm" viewBox="0 0 {width:g} {height:g}">',
           '<rect width="100%" height="100%" fill="#fff"/>',
           f'<text x="{width/2:g}" y="{margin+8:g}" text-anchor="middle" font-family="sans-serif" font-size="6" fill="#243447">{html.escape(title)}</text>',
           f'<text x="{grid_x:g}" y="{grid_y-3:g}" font-family="sans-serif" font-size="2.7" fill="#65788a">{paper.upper()} • {orientation.upper()}</text>',
           f'<rect x="{grid_x:g}" y="{grid_y:g}" width="{grid_w:g}" height="{header_h+grid_h:g}" rx="1" fill="none" stroke="#23384d" stroke-width=".3"/>']
    for col, label in enumerate(headers):
        x = grid_x + col * cell_w
        out += [f'<rect x="{x:g}" y="{grid_y:g}" width="{cell_w:g}" height="{header_h:g}" fill="#edf2f5" stroke="#536574" stroke-width=".22"/>',
                f'<text x="{x+cell_w/2:g}" y="{grid_y+6:g}" text-anchor="middle" font-family="sans-serif" font-size="2.7" fill="#243447">{label}</text>']
    for i in range(date_rows + 1):
        y = grid_y + header_h + i * cell_h
        out.append(f'<path d="M{grid_x:g} {y:g}H{grid_x+grid_w:g}" fill="none" stroke="#536574" stroke-width=".25"/>')
    for i in range(8):
        x = grid_x + i * cell_w
        out.append(f'<path d="M{x:g} {grid_y+header_h:g}V{grid_y+header_h+grid_h:g}" fill="none" stroke="#536574" stroke-width=".25"/>')
    if not blank:
        values, _ = month_grid(year, month, week_start, grid_mode)
        for idx, day in enumerate(values):
            if day is not None:
                col, row = idx % 7, idx // 7
                out.append(f'<text x="{grid_x+col*cell_w+2.5:g}" y="{grid_y+header_h+row*cell_h+5:g}" font-family="sans-serif" font-size="3" fill="#243447">{day}</text>')
    if notes:
        note_y = margin + note_h
        out.append(f'<text x="{grid_x:g}" y="{note_y+3:g}" font-family="sans-serif" font-size="2.6" fill="#65788a">NOTES</text>')
        for i in range(2):
            y = note_y + 8 + i * 7
            out.append(f'<path d="M{grid_x:g} {y:g}H{grid_x+grid_w:g}" stroke="#c4ccd2" stroke-width=".2"/>')
    out.append('</svg>')
    return '\n'.join(out)

def pdf_escape(value):
    return str(value).replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

def make_pdf(year, month, week_start=0, blank=False, rows=6, paper='a4', orientation='portrait', margin=8.0, notes=True, grid_mode='fixed'):
    wmm, hmm = page_dimensions(paper, orientation)
    scale = 72.0 / 25.4
    w, h, m = wmm*scale, hmm*scale, float(margin)*scale
    note_h = 22*scale if notes else 0
    values, date_rows = ([None]*(rows*7), rows) if blank else month_grid(year, month, week_start, grid_mode)
    grid_x, grid_bottom = m, m + note_h + 8*scale
    grid_w = w - 2*m
    header_h = 9*scale
    grid_top = h - m - 30*scale
    grid_h = grid_top - grid_bottom - header_h
    cell_w, cell_h = grid_w/7, grid_h/date_rows
    title = 'Undated Calendar' if blank else f'{MONTHS[month-1]} {year}'
    commands = ['0.25 w', '0 0 0 RG', '0 0 0 rg']
    commands += ['BT /F1 16 Tf', f'{w/2-55:.2f} {h-m-20:.2f} Td ({pdf_escape(title)}) Tj ET']
    y0 = grid_bottom
    commands += [f'{grid_x:.2f} {y0:.2f} {grid_w:.2f} {grid_h+header_h:.2f} re S']
    for i in range(8):
        x = grid_x + i*cell_w
        commands += [f'{x:.2f} {y0:.2f} m {x:.2f} {grid_top:.2f} l S']
    for i in range(date_rows+1):
        y = y0 + i*cell_h
        commands += [f'{grid_x:.2f} {y:.2f} m {grid_x+grid_w:.2f} {y:.2f} l S']
    commands += [f'{grid_x:.2f} {grid_top:.2f} m {grid_x+grid_w:.2f} {grid_top:.2f} l S']
    for col, label in enumerate(HEADERS[week_start]):
        x = grid_x + (col+.5)*cell_w - 8
        commands += [f'BT /F1 8 Tf {x:.2f} {grid_top+5:.2f} Td ({label}) Tj ET']
    if not blank:
        for idx, day in enumerate(values):
            if day is not None:
                col, row = idx%7, idx//7
                x = grid_x + col*cell_w + 4
                y = grid_top - header_h - (row+1)*cell_h + cell_h - 12
                commands += [f'BT /F1 8 Tf {x:.2f} {y:.2f} Td ({day}) Tj ET']
    if notes:
        commands += [f'BT /F1 7 Tf {grid_x:.2f} {m+note_h-8:.2f} Td (NOTES) Tj ET']
        for i in range(2):
            y = m + note_h - (13+i*12)*scale
            commands += [f'{grid_x:.2f} {y:.2f} m {grid_x+grid_w:.2f} {y:.2f} l S']
    stream = '\n'.join(commands).encode('ascii')
    objs = [
        b'<< /Type /Catalog /Pages 2 0 R >>',
        b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
        f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {w:.2f} {h:.2f}] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>'.encode('ascii'),
        b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
        b'<< /Length '+str(len(stream)).encode('ascii')+b' >>\nstream\n'+stream+b'\nendstream'
    ]
    pdf = bytearray(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n')
    offsets = [0]
    for i, obj in enumerate(objs, start=1):
        offsets.append(len(pdf)); pdf.extend(f'{i} 0 obj\n'.encode('ascii')); pdf.extend(obj); pdf.extend(b'\nendobj\n')
    xref = len(pdf)
    pdf.extend(f'xref\n0 {len(objs)+1}\n0000000000 65535 f \n'.encode('ascii'))
    for offset in offsets[1:]: pdf.extend(f'{offset:010d} 00000 n \n'.encode('ascii'))
    pdf.extend(f'trailer\n<< /Size {len(objs)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode('ascii'))
    return bytes(pdf)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--year', type=int, default=2027)
    parser.add_argument('--month', type=int)
    parser.add_argument('--all-months', action='store_true')
    parser.add_argument('--week-start', choices=['monday', 'sunday'], default='monday')
    parser.add_argument('--paper-size', choices=['a4', 'letter'], default='a4')
    parser.add_argument('--orientation', choices=['portrait', 'landscape'], default='portrait')
    parser.add_argument('--grid-mode', choices=['fixed', 'natural'], default='fixed')
    parser.add_argument('--margin', type=float, default=8.0, help='Printable margin in millimeters')
    parser.add_argument('--no-notes', action='store_true')
    parser.add_argument('--blank', action='store_true')
    parser.add_argument('--rows', type=int, choices=[5, 6], default=6)
    parser.add_argument('--format', choices=['svg', 'pdf'], default='svg')
    parser.add_argument('--out', default='generated')
    args = parser.parse_args()
    if not 0 <= args.margin <= 35:
        parser.error('--margin must be between 0 and 35 mm')
    week_start = 0 if args.week_start == 'monday' else 6
    target = Path(args.out); target.mkdir(parents=True, exist_ok=True)
    months = range(1, 13) if args.all_months else [args.month or 1]
    for month in months:
        name = 'blank' if args.blank else f'{calendar.month_name[month].lower()}-{args.year}'
        content = make_svg(args.year, month, week_start, args.blank, args.rows, args.paper_size, args.orientation, args.margin, not args.no_notes, args.grid_mode) if args.format == 'svg' else make_pdf(args.year, month, week_start, args.blank, args.rows, args.paper_size, args.orientation, args.margin, not args.no_notes, args.grid_mode)
        (target/f'{name}-{args.week_start}.{args.format}').write_bytes(content.encode('utf-8') if isinstance(content, str) else content)

if __name__ == '__main__':
    main()
