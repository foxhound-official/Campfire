from dataclasses import dataclass


@dataclass(slots=True)
class Character:
    character_id: str
    name: str
    character_class: str
    level: int

    current_hp: int
    max_hp: int

    armor_class: int
    initiative: int

    def __post_init__(self) -> None:
        if not self.character_id.strip():
            raise ValueError("character_id не может быть пустым")

        if not self.name.strip():
            raise ValueError("Имя персонажа не может быть пустым")

        if not self.character_class.strip():
            raise ValueError("Класс персонажа не может быть пустым")

        if self.level < 1:
            raise ValueError("Уровень персонажа должен быть не меньше 1")

        if self.max_hp < 1:
            raise ValueError("Максимальное здоровье должно быть больше 0")

        if not 0 <= self.current_hp <= self.max_hp:
            raise ValueError(
                "Текущее здоровье должно находиться "
                "в диапазоне от 0 до max_hp"
            )

        if self.armor_class < 0:
            raise ValueError("Класс брони не может быть отрицательным")
