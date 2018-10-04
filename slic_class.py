import numpy as np
import cv2
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
from PIL import Image, ImageFilter
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

import skimage.data
import skimage.color
import skimage.filters
import skimage.util
import skimage.segmentation
import pickle
# from skimage import io; io.use_plugin('pil')
# import matplotlib.pyplot as plt; plt.imread('myimage.png');


#def __init__(self, target_img, n_segments, compactness, sparseness, hash):
    #
    #
    #     self.target_img = target_img
    #     self.n_segments = n_segments  # スーパーピクセルの粒度。厳密にはぴったりこれと同じ数にはならない。
    #     self.compactness = compactness  # スーパーピクセルのパラメータ。多分ピクセルの大きさに関わる。よくわかってないけど多分５０で変えなくていい。
    #     self.sparseness = sparseness  # 絵文字の大きさを変え重なり具合を調節するパラメータ。基本0.3~0.5くらい。segmentによって変化させる。
    #
    #     if hash == 0:
    #         self.pickled_hash = 'notomoji/hash/alpha/step5_type_top10_emojis.pickle' #googleの絵文字かtwitterの絵文字をどちらか選ぶ。
    #     else:
    #         pickled_hash = 'twemoji/hash/alpha/step5_type_top10_emojis.pickle'  # googleの絵文字かtwitterの絵文字をどちらか選ぶ。
    #





def slic(target_img, n_segments, compactness, sparseness, hash):
    if hash == 0:
        pickled_hash = 'notomoji/hash/alpha/step5_type_top10_emojis.pickle'  # googleの絵文字かtwitterの絵文字をどちらか選ぶ。
    else:
        pickled_hash = 'twemoji/hash/alpha/step5_type_top10_emojis.pickle'  # googleの絵文字かtwitterの絵文字をどちらか選ぶ。


    if pickled_hash == 'notomoji/hash/alpha/step5_type_top10_emojis.pickle':
        emoji_siz = 128
    if pickled_hash == 'twemoji/hash/alpha/step5_type_top10_emojis.pickle':
        emoji_siz = 72

    emoji_siz2 = int(emoji_siz/2)

    img = cv2.imread(target_img, 1)


    a = skimage.segmentation.slic(img, n_segments=n_segments, compactness=compactness)
    img_sp = skimage.segmentation.mark_boundaries(img, a)


    siz = np.zeros(a.max())
    index = np.zeros([a.max(),2])
    col_av = np.zeros([a.max(),3])
    print(img.shape)


    for i in range(a.max()):
        siz[i] = a[a == i].size
        ind = np.where(a == i)
        ind = np.array(ind)
        index[i,:] = np.sum(ind.T, axis=0)
        col_av[i,:] = np.sum(img[a == i,:],axis=0)


    siz_av = np.sum(siz)/a.max()
    col_av = np.round(col_av/siz[:,np.newaxis])
    col_av = np.trunc(col_av/10)*10
    print(siz_av)


    ampli = int(Decimal(np.sqrt(emoji_siz*emoji_siz*sparseness/siz_av)).quantize(Decimal('0')))
    index = (np.round(ampli*index/siz[:,np.newaxis]) + emoji_siz2).astype(np.int32)
    con_img = np.zeros([img.shape[0]*ampli+emoji_siz,img.shape[1]*ampli+emoji_siz,4], dtype='u1')


    print(index)
    print(col_av)


    with open(pickled_hash, 'rb') as f:
        hash_dict = pickle.load(f)

    print(a.max())
    for i in range(a.max()):
        print(i)
        rgb = str(int(col_av[i,0])).zfill(3) + str(int(col_av[i,1])).zfill(3) + str(int(col_av[i,2])).zfill(3)
        #rgb = '020240040'  # g:020 b:240 r:040 に対応する絵文字を引っ張ってくる。str型。

        if pickled_hash == 'notomoji/hash/alpha/step5_type_top10_emojis.pickle':
            emoji = Image.open('notomoji/notomoji128/' + str(hash_dict[rgb][0])).convert("RGBA")  # RGBAに変換
        if pickled_hash == 'twemoji/hash/alpha/step5_type_top10_emojis.pickle':
            emoji = Image.open('twemoji/twemoji72x72/' + str(hash_dict[rgb][0])).convert("RGBA")  # RGBAに変換
        print(rgb)
        print(hash_dict[rgb][0])
        emoji = np.array(emoji)
        con_img[index[i,0]-emoji_siz2:index[i,0]+emoji_siz2, index[i,1]-emoji_siz2:index[i,1]+emoji_siz2][emoji[:,:,3] != 0] = emoji[emoji[:,:,3] != 0]


    #con_img = Image.fromarray(con_img[emoji_siz2:con_img.shape[0]-emoji_siz2,emoji_siz2:con_img.shape[1]-emoji_siz2,:], 'RGBA')
    return con_img



