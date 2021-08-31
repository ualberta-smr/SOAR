import os
import unittest

from pattern_mining.helper import is_torch_model_class
from pattern_mining.torch_model_diff import TorchModelDiff


class PatternMinerTest(unittest.TestCase):

    def test_is_torch_model_class(self):
        # filepath = 'autotesting/benchmarks_tf/alexnet.py'
        # fileminer = FileMiner(filepath)
        # is_model = is_torch_model_class(fileminer.classes[0])
        # self.assertTrue(is_model)
        pass

    def test_habijabi(self):
        # fm = FileMiner(os.path.abspath('../autotesting/benchmarks_tf/conv.py')
        #                , '../autotesting/benchmarks_tf/', 'autotesting/benchmarks_tf')
        # differ = TorchModelDiff(fm.classes[0])
        # diff = differ.get_diff()
        # print(diff)
        pass


if __name__ == '__main__':
    unittest.main()
