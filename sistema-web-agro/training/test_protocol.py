import json
import tempfile
import unittest
from datetime import date,timedelta
from pathlib import Path
from protocol import prepare,eligibility

class ProtocolTests(unittest.TestCase):
    def make(self,gap=False):
        rows=[]
        for i in range(40):
            d=date(2025,8,4)+timedelta(weeks=i)
            rows.append(['uva','US',d.isoformat(),None if gap and d==date(2026,4,13) else 3+i/100,100,300,'observed_partial'])
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        p=Path(self.tmp.name)/'snapshot.json';p.write_text(json.dumps({'weekly_rows':rows}));return p
    def test_cutoff_and_holdout_disjoint(self):
        train,test=prepare(self.make(),'uva','US','unit_fob',4)
        self.assertEqual(test[-1]['timestamp'],'2026-04-20')
        self.assertLess(train[-1]['timestamp'],test[0]['timestamp'])
        self.assertEqual(len(test),4)
        self.assertFalse(set(r['timestamp'] for r in train)&set(r['timestamp'] for r in test))
    def test_missing_history_not_imputed(self):
        with self.assertRaises(ValueError):prepare(self.make(True),'uva','US','unit_fob',1)
    def test_no_cross_series(self):
        with self.assertRaises(ValueError):prepare(self.make(),'palta','US','unit_fob',1)
    def test_select_an_earlier_validation_end(self):
        train,test=prepare(self.make(),'uva','US','unit_fob',4,'2026-03-30')
        self.assertEqual(test[-1]['timestamp'],'2026-03-30')
        self.assertLess(train[-1]['timestamp'],test[0]['timestamp'])
    def test_reserved_test_period_cannot_be_selected(self):
        with self.assertRaisesRegex(ValueError,'reservado'):
            prepare(self.make(),'uva','US','unit_fob',4,'2026-05-04')
    def test_eligibility_explains_gaps_without_filling_them(self):
        info=eligibility(self.make(True),'uva','US','unit_fob',4)
        self.assertFalse(info['ready'])
        self.assertEqual(info['consecutive_weeks'],1)
        self.assertTrue(info['eligible_validation_ends'])
        self.assertNotIn('2026-04-20',info['eligible_validation_ends'])
    def test_invalid_horizon_does_not_create_a_split(self):
        with self.assertRaises(ValueError):prepare(self.make(),'uva','US','unit_fob',3)

if __name__=='__main__':unittest.main()
