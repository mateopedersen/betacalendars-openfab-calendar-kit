#!/usr/bin/env python3
"""Dependency-free SVG calendar generator for the OpenFab Calendar Kit."""
import argparse, calendar, html
from pathlib import Path
MONTHS=list(calendar.month_name)[1:]
def make_svg(year,month,week_start=0,blank=False,rows=6,width=190,height=260):
    margin=8;gx=margin;gw=width-2*margin;gy=30;gh=height-55;head=9;cw=gw/7;rh=gh/rows
    title='Undated Calendar' if blank else f'{MONTHS[month-1]} {year}'
    z=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}mm" height="{height}mm" viewBox="0 0 {width} {height}">','<rect width="100%" height="100%" fill="white"/>',f'<text x="{width/2}" y="18" text-anchor="middle" font-family="sans-serif" font-size="6">{html.escape(title)}</text>']
    headers=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'] if week_start==0 else ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
    for i,h in enumerate(headers):z.append(f'<text x="{gx+(i+.5)*cw}" y="{gy+6}" text-anchor="middle" font-family="sans-serif" font-size="3">{h}</text>')
    for i in range(8):z.append(f'<path d="M{gx+i*cw} {gy+head}V{gy+head+gh}" stroke="#536574" stroke-width=".25"/>')
    for i in range(rows+1):z.append(f'<path d="M{gx} {gy+head+i*rh}H{gx+gw}" stroke="#536574" stroke-width=".25"/>')
    if not blank:
        offset=(calendar.monthrange(year,month)[0]-week_start)%7
        for n in range(offset+calendar.monthrange(year,month)[1]):
            day=n-offset+1
            if day>0:
                col=n%7;row=n//7
                z.append(f'<text x="{gx+col*cw+2}" y="{gy+head+row*rh+5}" font-family="sans-serif" font-size="3">{day}</text>')
    return '\n'.join(z+['</svg>'])
def main():
    p=argparse.ArgumentParser();p.add_argument('--year',type=int,default=2027);p.add_argument('--month',type=int);p.add_argument('--all-months',action='store_true');p.add_argument('--week-start',choices=['monday','sunday'],default='monday');p.add_argument('--blank',action='store_true');p.add_argument('--rows',type=int,choices=[5,6],default=6);p.add_argument('--out',default='generated');a=p.parse_args();Path(a.out).mkdir(parents=True,exist_ok=True);ws=0 if a.week_start=='monday' else 6
    months=range(1,13) if a.all_months else [a.month or 1]
    for m in months:
        name='blank' if a.blank else f'{calendar.month_name[m].lower()}-{a.year}'
        (Path(a.out)/f'{name}-{a.week_start}.svg').write_text(make_svg(a.year,m,ws,a.blank,a.rows),encoding='utf-8')
if __name__=='__main__':main()
