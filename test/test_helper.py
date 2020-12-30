import unittest
import numpy as np
from hevapy.helper import _convert_2d_np


class TestHelper(unittest.TestCase):
    def test(self):

        fun = _convert_2d_np
        set_val = self.set_val()
        get_val = self.get_val()

        for i in range(len(set_val)):
            assert fun(set_val[i]).shape == get_val[i].shape

    def set_val(self):
        val1 = np.array([1, 2, 4])
        val2 = np.array([])
        val3 = np.array([[1, 2, 3], [2, 3, 4]])

        return [val1, val2, val3]

    def get_val(self):
        val1 = np.array([1, 2, 4]).reshape(3, 1)
        val2 = np.array([]).reshape(0, 1)
        val3 = np.array([[1, 2, 3], [2, 3, 4]]).reshape(2, 3)

        return [val1, val2, val3]
