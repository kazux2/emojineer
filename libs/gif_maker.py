from PIL import Image, ImageDraw
from os import listdir
from os.path import isfile, join

tname = 'hokusai'
dir_path = 'emojineer/target_img/{}'.format(tname)
file_names = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
file_names.sort(reverse=False)

images = []
is_first = True
w, h = 0, 0
for file_name in file_names:
    if file_name == ".DS_Store":
        continue
    im = Image.open(join(dir_path, file_name))
    if is_first:
        w = im.size[0]
        h = im.size[1]
        is_first = False

    im = im.resize((w//2,h//2), Image.ANTIALIAS)
    images.append(im)

images[0].save('emojineer/gifs/{}.gif'.format(tname),
               save_all=True, append_images=images[1:], optimize=False, duration=200, loop=0)


