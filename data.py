from __future__ import annotations

import json

from typing_extensions import NotRequired, TypedDict

CharacterKey = str


class Character(TypedDict):
    name: str
    description: str | None
    canUseGeneralPotentialItem: bool
    canUseActivityPotentialItem: bool
    potentialItemId: str | None
    classicPotentialItemId: str | None
    nationId: str | None
    groupId: str | None
    teamId: str | None
    displayNumber: str | None
    appellation: str
    position: str
    tagList: list[str] | None
    itemUsage: str | None
    itemDesc: str | None
    itemObtainApproach: str | None
    isNotObtainable: bool
    isSpChar: bool
    maxPotentialLevel: int
    rarity: str
    profession: str
    subProfessionId: str
    trait: Trait | None
    phases: list[dict]
    skills: list[dict]
    displayTokenDict: dict | None
    talents: list[dict] | None
    potentialRanks: list[dict]
    favorKeyFrames: list[dict] | None
    allSkillLvlup: list[dict]


class Trait(TypedDict):
    candidates: list[TraitItem]


class TraitItem(TypedDict):
    unlockCondition: NotRequired[UnlockCondition]
    requiredPotentialRank: NotRequired[int]
    blackboard: NotRequired[list[BlackboardItem]]
    overrideDescription: str | None
    prefabKey: str | None
    rangeId: str | None


class UnlockCondition(TypedDict):
    phase: str
    level: int


class BlackboardItem(TypedDict):
    key: str
    value: float
    valueStr: str | None


with open('excel/character_table.json', encoding='utf8') as f:
    character_table: dict[CharacterKey, Character] = json.load(f)
