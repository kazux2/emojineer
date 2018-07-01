import unittest

from libs.rgbvalue_reduce_machine import RGBvalueReduceMachine


class testRGBvalueReduceMachine(unittest.TestCase):

	def setUp(self):
		self.machine5 = RGBvalueReduceMachine(unit=5)
		self.machine10 = RGBvalueReduceMachine(unit=10)
		self.machine20 = RGBvalueReduceMachine(unit=20)

	def test_value_reducer(self):
		self.assertEqual(self.machine5.value_reducer(233), 235)
		self.assertEqual(self.machine10.value_reducer(233), 230)
		self.assertEqual(self.machine20.value_reducer(233), 240)

		self.assertEqual(self.machine20.value_reducer(255), 255)

	def test_rgb_value_reducer(self):
		self.assertEqual(self.machine5.rgb_value_reducer([104,28,254]), [105,30,255])
