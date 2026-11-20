import unittest
from datetime import date
from unittest.mock import patch
import requests
from services import market_context as feed

TABLE = """<h1>Fecha: 20/11/2026</h1><table><tr><td>Producto</td><td>Variedad</td><td>Precio (S/. x Kg., S/. x Lt. o S/. x Unid.)</td></tr><tr><td rowspan=2>Palta</td><td>Palta Fuerte</td><td>8.45</td></tr><tr><td>Palta Hall</td><td>2.35</td></tr><tr><td>Uva</td><td>Uva Red Globe</td><td>3.75</td></tr></table>"""
class MarketContextTests(unittest.TestCase):
 def test_rowspan_retains_product_and_variety(self):
  rows=feed.parse_sisap(TABLE,date(2026,11,20))
  self.assertEqual([(r['product'],r['variety'],r['value']) for r in rows],[('Palta','Palta Fuerte',8.45),('Palta','Palta Hall',2.35),('Uva','Uva Red Globe',3.75)])
 def test_reject_wrong_date_or_changed_units(self):
  for html in [TABLE.replace('20/11/2026','19/11/2026'),TABLE.replace('Kg.','cajas')]:
   with self.assertRaises(ValueError):feed.parse_sisap(html,date(2026,11,20))
 def test_missing_values_never_become_zero(self):
  rows=feed.parse_sisap(TABLE.replace('8.45','n.d.').replace('2.35','NaN'),date(2026,11,20))
  self.assertEqual(len(rows),1);self.assertEqual(rows[0]['product'],'Uva')
 def test_failure_preserves_value_and_observation_date_as_stale(self):
  previous=[dict(id='usd',group='bcrp',value=3.4,observed_at='2026-11-19',last_success_at='2026-11-19T10:00:00-05:00')]
  def fail():raise requests.Timeout()
  row=feed.collect_one('bcrp',fail,previous)[0]
  self.assertEqual(row['value'],3.4);self.assertEqual(row['observed_at'],'2026-11-19');self.assertEqual(row['status'],'stale')
  self.assertEqual(previous[0]['value'],3.4)
 def test_first_failure_explicitly_unavailable(self):
  def fail():raise requests.Timeout()
  row=feed.collect_one('sisap',fail,[])[0]
  self.assertIsNone(row['value']);self.assertIsNone(row['observed_at']);self.assertEqual(row['status'],'unavailable')
 def test_snapshot_does_not_expose_mutable_cache(self):
  with patch.object(feed,'_state',{'items':[dict(id='a',value=4,status='stale')]}):
   row=feed.snapshot();row['items'][0]['value']=0
   self.assertEqual(feed.snapshot()['items'][0]['value'],4)
if __name__=='__main__':unittest.main()
