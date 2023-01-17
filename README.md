# Update Pipeline

## Before you begin

+ Get the latest Arknights install package.

+ Get [UnityPy](https://github.com/K0lb3/UnityPy) via `pip install UnityPy`.

## Step 1: Update Excel

1. Download the latest json file `excel/charword_table.json` and `excel/character_table.json`
   from [ArknightsGameData](https://github.com/Kengxxiao/ArknightsGameData/tree/master/zh_CN/gamedata/).

   _TODO: make the download process automatic._

2. Put the downloaded json file into the `excel/new/` folder.

3. Run `python update_json.py` and the script will overwrite the old json file and output new character keys to `stdout`
   and `update.txt`.

## Step 2: Update Avatar

1. Extract `spritepack/ui_char_avatar_h1_0.ab` from the game package to the `ab/` folder.

2. Extract **all** assets (Sprite & Texture2D) from the file mentioned above.

3. Put images named like `SpriteAtlasTexture-.*.png` to `image/raw-avatar/Atlas` and the rest to `image/raw-avatar/`.

4. Run `python process_avatar.py`. The script will ask you to match each Atlas image with its corresponding
   alpha mask image then output new character avatars to `image/avatar/` and the number of new avatars.

## Step 3: Update Portrait

1. Extract **all** files under `arts/charportraits/` from the game package to the `ab/` folder.

2. Extract **all** assets (MonoBehavior & Texture2D) from the file mentioned above.

3. Put extracted images and json files to `image/raw-portrait/`.

4. Run `python process_portrait.py`. The script will output portraits to `image/portrait/`.

## ~~Step 4: Update Tachie(立绘) [Invalid]~~

1. Extract `charpack/{new_character_key}.ab` to `ab/alpha/`.

   **Note: After 2022-08-12, we cannot find tachie resources in .ab files mentioned above.**

2. Run `python update_tachie.py`. The script will output new tachie to `image/tachie/` and `update/`.

## Step 5: Update Recruit [Optional]

1. Manually get new recruitable character names from [Arknights-Bilibili](https://space.bilibili.com/161775300/dynamic).

2. Edit required names in `update_recruit.py` and run `python update_recruit.py`. The script will
   update `excel/recruit_table.json` and keep an original copy of the old one.

## Step 6: Update Voice [Optional & Deprecated]

## Step 7: Check Update Integrity [Optional]