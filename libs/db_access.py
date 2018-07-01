import json
import os
pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from peewee import *

# Connect to a Postgres database.
db = PostgresqlDatabase('postgres', user='postgres', password='example', host='localhost', port=5432)

class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = db

class W1x1RGBtoEmojiname(BaseModel):
    rgb_value = CharField(unique=True)
    emoji_file_name = CharField()


class NumtoWEmoji(BaseModel):
    id = IntegerField(unique=True)
    emoji_file_name = CharField()


class W1x1RGBtoIdx(BaseModel):
    rgb_value = CharField(unique=True)
    emoji_num = IntegerField()


if __name__ == "__main__":
    db.connect()
    db.create_tables([NumtoWEmoji, W1x1RGBtoIdx])

    with open('{}/{}'.format(pardir, 'data/num_wemoji_dict.json'), 'r') as f:
        num_wemoji_dict = json.load(f)

    for key, value in num_wemoji_dict.items():
        record_num, created = NumtoWEmoji.get_or_create(id=int(key), emoji_file_name=value)
        print(record_num, "th record created:",created)

    from os import listdir
    from os.path import isfile, join, splitext

    dir_path = '{}/data/w1x1_hash_dicts_0_256_5'.format(pardir)
    file_names = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]

    for file_name in file_names:
        if file_name == '.gitkeep':
            continue
        with open('{}/{}'.format(dir_path, file_name), 'r') as f:
            yo = json.load(f)
        fname, ext = os.path.splitext(file_name)
        record_num, created = W1x1RGBtoIdx.get_or_create(rgb_value=int(fname), emoji_num=yo[0])
        print(record_num, "th record created:", created)




