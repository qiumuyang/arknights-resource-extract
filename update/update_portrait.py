from __future__ import annotations

from pathlib import Path

from PIL import Image
from typing_extensions import TypedDict, NotRequired

from .extract_ab import extract_ab


class Atlas(TypedDict):
    image: Image.Image | None
    alpha: Image.Image | None
    composed: NotRequired[Image.Image]


class PortraitHub:

    def __init__(self, hub: dict):
        self.name_to_atlas = {x['name']: x['atlas'] for x in hub['_sprites']}
        self.name_to_position = {}
        self.atlas: list[Atlas] = [{
            'image': None,
            'alpha': None
        } for _ in range(max(self.name_to_atlas.values()) + 1)]

    def add_atlas(self, atlas_name: str, image: Image.Image):
        if atlas_name.count('#') != 1:
            raise ValueError('invalid atlas name: {}'.format(atlas_name))
        if atlas_name.endswith('a'):
            key = 'alpha'
            atlas_name = atlas_name[:-1]
        else:
            key = 'image'
        idx = int(atlas_name.split('#')[-1])
        try:
            self.atlas[idx][key] = image
        except IndexError as e:
            print("IndexError: {} {}".format(idx, atlas_name))

    def add_position(self, name: str, position: dict):
        for x in position['_sprites']:
            name = x['name']
            rect = x['rect']
            rotate = x['rotate']
            self.name_to_position[name] = {'rect': rect, 'rotate': rotate}

    @property
    def names(self):
        return list(self.name_to_atlas.keys())

    def compose(self, image: Image.Image, alpha: Image.Image) -> Image.Image:
        # find in self.atlas
        idx = [x['image'] for x in self.atlas].index(image)
        cached = self.atlas[idx].get('composed', None)
        if cached is None:
            r, g, b, _ = image.split()
            a, _, _, _ = alpha.resize(image.size).split()
            composed = Image.merge('RGBA', (r, g, b, a))
            self.atlas[idx]['composed'] = composed
            return composed
        return cached

    def get_portrait(self, name: str) -> Image.Image:
        atlas_id = self.name_to_atlas[name]
        image = self.atlas[atlas_id]['image']
        alpha = self.atlas[atlas_id]['alpha']
        rect, rotate = self.name_to_position[name].values()
        if image is None or alpha is None:
            raise RuntimeError(
                f'missing {"image" if image is None else "alpha"} for {name}')
        width, height = image.size
        w, h, x, y = rect['w'], rect['h'], rect['x'], rect['y']
        cropped = self.compose(image, alpha).crop(
            (x, height - y - h, x + w, height - y))
        return cropped if not rotate else cropped.transpose(Image.ROTATE_270)


def update_portrait(
        portrait_ab_dir: Path,
        output_dir: Path = Path('image/portrait')) -> list[str]:
    portrait_ab_paths = list(portrait_ab_dir.glob('*.ab'))
    assert 'portrait_hub.ab' in [x.name for x in portrait_ab_paths]
    pack_paths = [x for x in portrait_ab_paths if x.name != 'portrait_hub.ab']
    hub_path = [x for x in portrait_ab_paths if x.name == 'portrait_hub.ab'][0]

    # set up portrait hub
    _, hub_dict = list(extract_ab(str(hub_path), ['MonoBehaviour']))[0]
    hub = PortraitHub(hub_dict)
    for pack in pack_paths:
        # add image
        for reader, result in extract_ab(str(pack), ['Texture2D']):
            hub.add_atlas(reader.read().name, result)
        # add position data for crop
        for reader, result in extract_ab(str(pack), ['MonoBehaviour']):
            hub.add_position(reader.read().name, result)

    existing = [x.stem for x in output_dir.glob('*.png')]
    update = []
    for name in hub.names:
        if name not in existing:
            hub.get_portrait(name).save(output_dir / (name + '.png'))
            update.append(name)
    return update
