import calendar
import importlib.util
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT=Path(__file__).parents[1]
spec=importlib.util.spec_from_file_location('calendar_kit',ROOT/'generator/calendar_kit.py')
kit=importlib.util.module_from_spec(spec);spec.loader.exec_module(kit)

class CalendarTests(unittest.TestCase):
 def test_leap_years(self):
  for year,want in [(1900,False),(2000,True),(2024,True),(2027,False),(2100,False),(2400,True)]:
   self.assertEqual(calendar.isleap(year),want)
 def test_2027_dates_and_month_lengths(self):
  self.assertEqual(sum(calendar.monthrange(2027,m)[1] for m in range(1,13)),365)
  for month in range(1,13):
   for start in (0,6):
    tree=ET.fromstring(kit.make_svg(2027,month,start))
    nums=[int(t.text) for t in tree.iter('{http://www.w3.org/2000/svg}text') if t.text and t.text.isdigit()]
    self.assertEqual(nums,list(range(1,calendar.monthrange(2027,month)[1]+1)))
 def test_blank_has_no_date_numbers(self):
  tree=ET.fromstring(kit.make_svg(2027,1,blank=True))
  nums=[t.text for t in tree.iter('{http://www.w3.org/2000/svg}text') if t.text and t.text.isdigit()]
  self.assertEqual(nums,[])
 def test_calendar_stencil_cut_geometry(self):
  path=ROOT/'fabrication/laser/stencil/calendar-stencil-190x260.svg'
  tree=ET.parse(path); cut=next(g for g in tree.getroot() if g.attrib.get('id')=='CUT')
  rects=[e for e in cut if e.tag.endswith('rect')]
  self.assertEqual(len(rects),43) # outer profile + 42 date windows
  for e in rects:
   x=float(e.attrib['x']);y=float(e.attrib['y']);w=float(e.attrib['width']);h=float(e.attrib['height'])
   self.assertGreaterEqual(x,8);self.assertGreaterEqual(y,6)
   self.assertLessEqual(x+w,182);self.assertLessEqual(y+h,254)
  self.assertAlmostEqual(float(rects[1].attrib['width']),22.5714,places=3)
  self.assertAlmostEqual(float(rects[1].attrib['height']),27.6667,places=3)
  self.assertAlmostEqual(float(rects[1].attrib['x'])-8,2.0,places=3)
  self.assertAlmostEqual(182-float(rects[7].attrib['x'])-float(rects[7].attrib['width']),2.0,places=3)
 def test_broad_date_range_1900_2100(self):
  for year in range(1900,2101):
   for month in range(1,13):
    for start in (0,6):
     values,rows=kit.month_grid(year,month,start,'fixed')
     offset=(calendar.monthrange(year,month)[0]-start)%7
     dates=[n for n in values if n is not None]
     self.assertEqual(rows,6);self.assertEqual(len(values),42)
     self.assertEqual(dates,list(range(1,calendar.monthrange(year,month)[1]+1)))
     self.assertEqual(values.index(1),offset)
 def test_dxf_has_units_and_closed_openings(self):
  dxf=(ROOT/'fabrication/dxf/calendar-stencil-190x260.dxf').read_text()
  self.assertIn('AC1015',dxf);self.assertIn('$INSUNITS',dxf)
  self.assertEqual(dxf.count('LWPOLYLINE'),43)
  self.assertEqual(dxf.count('0.41421356'),168)
 def test_pdf_header_and_paper_dimensions(self):
  pdf=kit.make_pdf(2027,1)
  self.assertTrue(pdf.startswith(b'%PDF-1.4'))
  self.assertIn(b'/MediaBox [0 0 595.28 841.89]',pdf)

if __name__=='__main__': unittest.main()
