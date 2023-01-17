from typing import List

import UnityPy
from UnityPy import Environment
from UnityPy.files import ObjectReader


def mono_behaviour_extractor(obj: ObjectReader):
    assert obj.type.name == 'MonoBehaviour'
    if obj.serialized_type and obj.serialized_type.nodes:
        typetree = obj.read_typetree()
    else:
        raise RuntimeError(f'cannot read type tree for {obj.name}')
    return typetree


def image_extractor(obj: ObjectReader):
    assert obj.type.name == 'Texture2D' or obj.type.name == 'Sprite'
    return obj.read().image


extractor = {
    'MonoBehaviour': mono_behaviour_extractor,
    'Texture2D': image_extractor,
    'Sprite': image_extractor,
}


def search(item):
    ret = []
    if not isinstance(item, Environment) and getattr(item, "objects", None):
        # serialized file
        return [val for val in item.objects.values()]

    elif getattr(item, "files", None):  # WebBundle and BundleFile
        # bundle
        for item in item.files.values():
            ret.extend(search(item))
        return ret

    return ret


def extract_ab(path: str, types: List[str]):
    env = UnityPy.load(path)

    for reader in env.objects:
        if reader.type.name in types:
            yield reader, extractor[reader.type.name](reader)
        # if reader.type.name == 'AssetBundle':
        #     print(reader.read().m_Container)
