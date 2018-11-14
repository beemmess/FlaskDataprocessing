import unittest
import pandas as pd
import numpy as np
from shimmer import ShimmerFx

class InitialTestCase(unittest.TestCase):

    def testSomething(self):
        f = """1,1,3,1
        1,2,3,2
        """
        json_input = { "userId": "Cucumber", "features": "timestamp,GSR,PPG,task", "data": f}

        msg = ShimmerFx.avgGSRandPPG(json_input)
        df,features = ShimmerFx.convertToDataFrame(msg)
        avgGSR = df["avgGSR"].values[0]
        self.assertEqual(avgGSR, 1.5);

if __name__ == '__main__':
    unittest.main()
