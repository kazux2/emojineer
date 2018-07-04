
import json
import os, time
from os import listdir
from os.path import isfile, join
import pickle
from statistics import mean

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dir_path = '{}/data/w1x1_hash_dicts_0_256_5'.format(pardir)


# making picked hash dict
#
# file_names = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
#
# hash_dict = {}
# for file_name in file_names:
# 	root, ext = splitext(file_name)
# 	with open('{}/{}'.format(dir_path,file_name), 'r') as f:
# 		value = json.load(f)
#
# 	hash_dict[root] = value
#
#
# with open('{}/data/pickle_w1x1_hash_dicts_0_256_5'.format(pardir), 'wb') as f:
# 	pickle.dump(hash_dict, f)


'''
ピックル処理時間：35.04753112792969
ピックル処理時間：4.76837158203125
ピックル処理時間：4.0531158447265625
ピックル処理時間：2.86102294921875
ピックル処理時間：4.0531158447265625
ピックル処理時間平均：10.156631469726562

ファイルインポート処理時間：612.0204925537109
ファイルインポート処理時間：641.1075592041016
ファイルインポート処理時間：693.0828094482422
ファイルインポート処理時間：577.9266357421875
ファイルインポート処理時間：617.0272827148438
ファイルインポート処理時間平均：628.2329559326172
'''

with open('{}/data/pickle_w1x1_hash_dicts_0_256_5'.format(pardir), 'rb') as f:
	hash_dict = pickle.load(f)

namelist = ["040000100","240050100","110000200","090005105","200050100"]

# calc time with picked hash
timelist = []
for i in namelist:

	t1 = time.time()
	print(hash_dict[i])
	t2 = time.time()
	elapsed_time = t2 - t1
	timelist.append(elapsed_time)

for i in timelist:
	print(f"ピックル処理時間：{i*1000000}")


print(f"ピックル処理時間平均：{mean(timelist)*1000000}")


# calc time with hash .json
timelist2 = []
for i in namelist:
	t3 = time.time()
	with open('{}/{}.json'.format(dir_path, i), 'r') as f:
		w1x1_hash = json.load(f)
	print(w1x1_hash)
	t4 = time.time()
	elapsed_time = t4 - t3
	timelist2.append(elapsed_time)

for i in timelist2:
	print(f"ファイルインポート処理時間：{i*1000000}")


print(f"ファイルインポート処理時間平均：{mean(timelist2)*1000000}")

