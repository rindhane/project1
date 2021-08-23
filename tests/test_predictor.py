#! /usr/bin/env python
import unittest
import pandas as pd
import os  
from analysis_liveTrade.workers import Predictor

class TestPredictor(unittest.TestCase):
    def setUp(self):
        self.data=pd.read_json(os.path.dirname(__file__)+'/testfile.json')
        self.predictor=Predictor(data=self.data)
    def test_dataPresence(self):
        self.assertEqual(len(self.predictor.data),len(self.data))
    def test_prediction(self):
        self.predictor.nextVal()
    def tearDown(self):
        pass

if __name__=="__main__":
    unittest.main()