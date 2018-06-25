

class RGBvalueReduceMachine():
	'''
	[243,120,3] -> [245, 120, 5]
	'''

	def __init__(self, unit=20):
		self.unit = unit

	def value_reducer(self, r):
		q, mod = divmod(r, self.unit)
		if mod < self.unit/2:
				_r = 0
		else:
				_r = self.unit

		new_r = q * self.unit + _r

		if new_r > 255:
			new_r = 255 -(255 % self.unit)
		return new_r

	def rgb_value_reducer(self, rgblist):
		return [self.value_reducer(i) for i in rgblist]



