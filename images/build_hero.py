"""Build the exact vector concept cover from the project's canonical dimensions."""
from pathlib import Path
import calendar

OUT=Path(__file__).parent/'hero/concept-visualization.svg'
parts=['''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900"><defs><linearGradient id="bg" x2="0" y2="1"><stop stop-color="#f4f1e9"/><stop offset="1" stop-color="#e7e3d9"/></linearGradient><linearGradient id="wood" x2="0" y2="1"><stop stop-color="#d9b783"/><stop offset="1" stop-color="#b88a53"/></linearGradient><filter id="shadow"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#203246" flood-opacity=".17"/></filter></defs><rect width="1600" height="900" fill="url(#bg)"/><rect x="48" y="42" width="1504" height="816" rx="26" fill="#fbfaf6" stroke="#d3d0c8" stroke-width="2"/><text x="90" y="105" font-family="sans-serif" font-size="32" font-weight="700" fill="#24384d">BETACALENDARS OPENFAB CALENDAR KIT</text><text x="92" y="141" font-family="sans-serif" font-size="17" fill="#65798a">A parametric system for laser-cut stencil, pen plotting and paper planning</text><rect x="90" y="166" width="1420" height="1" fill="#d7d9d7"/>''']
# Canonical 190 x 260 mm stencil, scaled 1.72 px/mm.
scale=1.72;xoff=110;yoff=205
parts.append(f'<g transform="translate({xoff} {yoff}) scale({scale})" filter="url(#shadow)">')
parts.append('<rect x="8" y="6" width="174" height="248" rx="2" fill="url(#wood)" stroke="#765837" stroke-width="1.2"/><rect x="10" y="8" width="170" height="23" fill="#d7b17b" stroke="#856742" stroke-width=".45"/><text x="95" y="22" text-anchor="middle" font-family="sans-serif" font-size="4" fill="#24384d">MONTH / TITLE</text><line x1="8" y1="28" x2="182" y2="28" stroke="#24384d" stroke-width=".35"/><rect x="8" y="31" width="174" height="10" fill="#d0a76d" stroke="#765837" stroke-width=".35"/>')
for col,label in enumerate(['MON','TUE','WED','THU','FRI','SAT','SUN']):
 pitchx=(174-4+2)/7
 parts.append(f'<text x="{10+(col+.5)*pitchx:.4f}" y="37.5" text-anchor="middle" font-family="sans-serif" font-size="3.3" fill="#24384d">{label}</text>')
# date windows separated by 2 mm webs and surrounded by a 2 mm field margin
pitchx=(174-4+2)/7; pitchy=(180-4+2)/6; cellw=pitchx-2; cellh=pitchy-2
for row in range(6):
 for col in range(7):
  xx=10+col*pitchx; yy=43+row*pitchy
  parts.append(f'<rect x="{xx:.4f}" y="{yy:.4f}" width="{cellw:.4f}" height="{cellh:.4f}" rx="1" fill="#fbfaf6" stroke="#765837" stroke-width=".3"/>')
parts.append('<text x="8" y="228" font-family="sans-serif" font-size="3.5" fill="#24384d">NOTES</text><line x1="8" y1="230" x2="182" y2="230" stroke="#496073" stroke-width=".3"/><line x1="8" y1="241" x2="182" y2="241" stroke="#496073" stroke-width=".3"/><text x="95" y="252" text-anchor="middle" font-family="sans-serif" font-size="2.8" fill="#344a5d">190 × 260 mm • 42 windows • 2 mm bridges</text></g>')
# One real date example: Monday-first January 2027.
x0,y0,gw,gh=552,298,306,354;header=28;cw=gw/7;rh=gh/6
parts.append(f'<g filter="url(#shadow)"><rect x="520" y="205" width="370" height="520" rx="8" fill="#fff" stroke="#c9d1d5" stroke-width="2"/><text x="705" y="248" text-anchor="middle" font-family="sans-serif" font-size="26" font-weight="600" fill="#24384d">JANUARY 2027</text><text x="705" y="275" text-anchor="middle" font-family="sans-serif" font-size="13" fill="#65798a">A4 • Monday first • generated layout</text><rect x="{x0}" y="{y0}" width="{gw}" height="{gh+header}" rx="3" fill="#fff" stroke="#41566a" stroke-width="2"/>')
for col,label in enumerate(['MON','TUE','WED','THU','FRI','SAT','SUN']):
 xx=x0+col*cw
 parts.append(f'<rect x="{xx:.3f}" y="{y0}" width="{cw:.3f}" height="{header}" fill="#edf2f5" stroke="#8d9ca7" stroke-width="1"/><text x="{xx+cw/2:.3f}" y="{y0+19}" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#24384d">{label}</text>')
for col in range(8):
 xx=x0+col*cw;parts.append(f'<path d="M{xx:.3f} {y0+header}V{y0+header+gh}" stroke="#536574" stroke-width="1"/>')
for row in range(7):
 yy=y0+header+row*rh;parts.append(f'<path d="M{x0} {yy:.3f}H{x0+gw}" stroke="#536574" stroke-width="1"/>')
parts.append(f'<path d="M{x0} {y0+header+gh}H{x0+gw}" stroke="#536574" stroke-width="1"/>')
for index,day in enumerate(calendar.Calendar(firstweekday=calendar.MONDAY).itermonthdays(2027,1)):
 if day:
  row,col=divmod(index,7);parts.append(f'<text x="{x0+col*cw+8:.3f}" y="{y0+header+row*rh+20:.3f}" font-family="sans-serif" font-size="14" fill="#24384d">{day}</text>')
parts.append('</g>')
parts.append('<g transform="translate(1000 250)"><text x="210" y="0" text-anchor="middle" font-family="sans-serif" font-size="21" font-weight="600" fill="#24384d">PLOTTER + TOKEN WORKFLOW</text><g stroke="#40586b" stroke-width="9" fill="none"><path d="M35 48H390M55 48V130M370 48V130M55 130H370"/></g><path d="M210 130V195" stroke="#647b8d" stroke-width="9"/><path d="M210 195l-9 22h18z" fill="#263b50"/><path d="M90 250h250" stroke="#c1cbd0" stroke-width="2"/><text x="210" y="279" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#65798a">Pen paths and print layouts share the same date geometry.</text><rect x="35" y="330" width="355" height="158" rx="12" fill="#d5af78" stroke="#765837" stroke-width="3"/>')
for i in range(12):
 col,row=i%6,i//6;xx=55+col*52;yy=350+row*62
 parts.append(f'<rect x="{xx}" y="{yy}" width="42" height="44" rx="5" fill="#fbfaf6" stroke="#765837" stroke-width="2"/><text x="{xx+21}" y="{yy+29}" text-anchor="middle" font-family="sans-serif" font-size="19" font-weight="600" fill="#24384d">{i+1}</text>')
parts.append('<text x="212" y="515" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#65798a">Date-token sheet • 1–31 in the kit</text></g><text x="100" y="790" font-family="sans-serif" font-size="16" fill="#536779">Digital concept visualization based on the included drawings; no physical prototype is claimed.</text><text x="100" y="820" font-family="sans-serif" font-size="13" fill="#778894">SVG layer colors are conventions only. Verify material and machine settings locally.</text></svg>')
OUT.write_text(''.join(parts),encoding='utf-8')
