from __future__ import annotations

from pathlib import Path

from .extract_ab import extract_ab


def update_avatar_old(
    avatar_ab_path: Path,
    output_dir: Path = Path('image/avatar'),
) -> list[str]:
    existing = [x.stem for x in output_dir.iterdir()]
    update = []
    for reader, result in extract_ab(str(avatar_ab_path), ['Sprite']):
        # 'Texture2D' for SpriteAtlasTexture, ignored
        name = reader.read().name
        if name not in existing:
            update.append(name)
            result.save(output_dir / (name + '.png'))
    return update


def update_avatar(
    avatar_ab_dir: Path,
    output_dir: Path = Path('image/avatar'),
) -> list[str]:
    existing = [x.stem for x in output_dir.iterdir()]
    update = []
    for reader, result in extract_ab(str(avatar_ab_dir), types=['Sprite']):
        name = reader.read().name
        # filter non-level-0 avatars (ends with '_1+', '_1', '_2', '#1', etc.)
        # normal pattern: char_xxx_name
        # bad pattern: char_xxx_name_1, char_xxx_name_skin#1
        if len(name.split('_')) != 3:
            continue
        if name not in existing:
            update.append(name)
            result.save(output_dir / (name + '.png'))
    return update
