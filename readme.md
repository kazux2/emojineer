# emojineer
An image converter from a given image into an emoji collage.

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

## run emojineer for multiple images/similarities/conversions at once
prepare target images in `emojineer/target_img/` and edit under `if __name__ == '__main__':` in `main.py`.

`conversions` indicates how big splitting is and takes 0 to 1.
It must be a list of numbers like: `conversions = [0.2, 0.1, 0.08, 0.01] # 0 ~ 1`

`similarities` indicates ranks of similar emojis and takes 0 to 2613(because the number of emoji candidates is 2614).
It must be a list of numbers like: `similarities = [0, 10, 20, 500, 1000, 2000, 2500, 2600, 2610]`
