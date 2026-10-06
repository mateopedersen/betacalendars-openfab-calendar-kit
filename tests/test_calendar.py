import calendar, importlib.util, unittest
from pathlib import Path
p=Path(__file__).parents[1]/'generator/calendar_kit.py'
s=importlib.util.spec_from_file_location('calendar_kit',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class CalendarTests(unittest.TestCase):
 def test_leap_years(self):
  for y,want in [(1900,False),(2000,True),(2024,True),(2027,False),(2100,False),(2400,True)]: self.assertEqual(calendar.isleap(y),want)
 def test_month_days_all_2027(self):
  self.assertEqual(sum(calendar.monthrange(2027,x)[1] for x in range(1,13)),365)
  for month in range(1,13):
   for start in (0,6):
    svg=m.make_svg(2027,month,start)
    self.assertEqual(svg.count('<text'),calendar.monthrange(2027,month)[1]+8)
 def test_blank_no_numbers(self):
  s=m.make_svg(2027,1,blank=True)
  self.assertNotIn('>1</text>',s)
 def test_six_week_grid_lines(self):
  self.assertEqual(m.make_svg(2027,1).count('stroke="#536574"'),15)
if __name__=='__main__': unittest.main()
