
'''
[243,120,3] -> [245, 120, 5]
'''

def value_reducer(r):
	q, mod = divmod(r, 10)
	if mod < 5:
		if mod < 2.5:
			_r = 0
		else:
			_r = 5
	else:
		if mod < 7.5:
			_r = 5
		else:
			_r = 10

	new_r = q*10 + _r

	return new_r

def rgb_value_reducer(rgblist):
	return [value_reducer(i) for i in rgblist]

print(rgb_value_reducer([3,124,255]))

