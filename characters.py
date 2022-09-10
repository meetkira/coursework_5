from abc import ABC
from typing import Dict, Type

from skills import Skill, fury_punch, hard_shot


class Character(ABC):
    name: str = NotImplemented
    max_health: float = NotImplemented
    max_stamina: float = NotImplemented
    attack: float = NotImplemented
    stamina: float = NotImplemented
    armor: float = NotImplemented
    skill: Skill = NotImplemented


class Warrior(Character):
    name = "Воин"
    max_health = 60.0
    max_stamina = 30.0
    attack = 0.8
    stamina = 0.9
    armor = 1.2
    skill = fury_punch


class Thief(Character):
    name = "Вор"
    max_health = 50.0
    max_stamina = 25.0
    attack = 1.5
    stamina = 1.2
    armor = 1.0
    skill = hard_shot


characters: Dict[str, Type[Character]] = {
    Warrior.name: Warrior,
    Thief.name: Thief,
}
