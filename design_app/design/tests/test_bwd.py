import unittest

import ..bwd as bwd


class TestBWD(unittest.TestCase):
    def setUp(self):
        self.design = bwd.BWDRandomizer()

    def test_init(self):
        a = self.design.initial_state()
        self.assertEqual(a, {'w': [0] * 3})
    
    def test_assign(self):
        state = {'w': 0}
        covs = {'a': 1, 'b': 2, 'c': 3}
        a = self.design.assign(state, covs)
