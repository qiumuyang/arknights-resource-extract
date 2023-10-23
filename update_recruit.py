import json
from typing import Any, Dict

from data import character_table

profession_mapping = dict(
    zip(
        ['CASTER', 'MEDIC', 'PIONEER', 'SNIPER',
         'SUPPORT', 'SPECIAL', 'TANK', 'WARRIOR'],
        ['术师', '医疗', '先锋', '狙击',
         '辅助', '特种', '重装', '近卫']
    )
)


def get_recruit(name: str) -> Dict[str, Any]:
    c_dict = [item for item in character_table.values()
              if item['name'] == name][0]

    rarity = int(c_dict["rarity"][-1])
    tags = []
    if c_dict['position'] == 'MELEE':
        tags.append('近战位')
    if c_dict['position'] == 'RANGED':
        tags.append('远程位')
    if rarity == 6:
        tags.append('高级资深干员')
    if rarity == 5:
        tags.append('资深干员')
    return {
        'name': name,
        'type': profession_mapping[c_dict['profession']],
        'rarity': rarity,
        'tags': tags + c_dict['tagList']
    }


if __name__ == '__main__':
    # load the previous recruit table
    with open('excel/recruit_table.json', encoding='utf-8') as f:
        recruit_table = json.load(f)

    # keep a copy of the previous recruit table
    with open('excel/recruit_table_copy.json', 'w', encoding='utf-8') as f:
        json.dump(recruit_table, f, ensure_ascii=False, indent=4)

    # update
    names = ['棘刺', '安哲拉', '蜜蜡', '贾维', '孑']
    for _name in names:
        print(json.dumps(get_recruit(_name), ensure_ascii=False, indent=4), end=',\n')
        recruit_table.append(get_recruit(_name))

    # write back
    with open('excel/recruit_table.json', 'w', encoding='utf-8') as f:
        json.dump(recruit_table, f, ensure_ascii=False, indent=4)
