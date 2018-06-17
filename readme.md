# emojineer
An image converter from given images into emoji collage.

## set up
### pip install libraries
run `pip install -r requirements.txt`

### get emoji with the scraper
run `emoji_collector.py`. you'll get 2614 emojis in `data/emoji_apple`

### fill emoji's transparent background white
run `whiten_alpha.py`

### generate emoji's rgb data json
run `calc_average_rgb.py`

## run emojineer
prepare target image and edit `target_file_name` under `if __name__ == '__main__':` in `emojineer.py`.
run `emojineer.py`
