import os
import unittest

from pattern_mining.helper import is_torch_model_class


class PatternMinerTest(unittest.TestCase):

    def test_is_torch_model_class(self):
        filepath = 'autotesting/benchmarks_tf/alexnet.py'
        from pattern_mining.pattern_miner import FileMiner
        fileminer = FileMiner(filepath)
        is_model = is_torch_model_class(fileminer.classes[0])
        self.assertTrue(is_model)


if __name__ == '__main__':
    unittest.main()
