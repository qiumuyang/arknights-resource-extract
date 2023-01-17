from pathlib import Path
from typing import List

from .extract_ab import extract_ab


def update_avatar(avatar_ab_path: Path, output_dir: Path = Path('image/avatar')) -> List[str]:
    existing = [x.stem for x in output_dir.iterdir()]
    update = []
    for reader, result in extract_ab(str(avatar_ab_path), ['Sprite']):  # 'Texture2D' for SpriteAtlasTexture, ignored
        name = reader.read().name
        if name not in existing:
            update.append(name)
            result.save(output_dir / (name + '.png'))
    return update
