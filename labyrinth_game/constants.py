# Ключи game_state
PLAYER_INVENTORY = "player_inventory"
CURRENT_ROOM = "current_room"
GAME_OVER = "game_over"
STEPS_TAKEN = "steps_taken"

# Названия комнат
ENTRANCE = "entrance"
HALL = "hall"
TRAP_ROOM = "trap_room"
LIBRARY = "library"
ARMORY = "armory"
TREASURE_ROOM = "treasure_room"
LABORATORY = "laboratory"
STORAGE_ROOM = "storage_room"


ROOMS = {
    ENTRANCE: {
        "description": "Вы в темном входе лабиринта...",
        "exits": {"north": HALL, "east": TRAP_ROOM},
        "items": ["torch"],
        "puzzle": None,
    },
    HALL: {
        "description": "Большой зал с эхом. По центру стоит пьедестал с запечатанным сундуком.",  # noqa: E501
        "exits": {
            "south": ENTRANCE,
            "west": LIBRARY,
            "north": TREASURE_ROOM,
            "east": STORAGE_ROOM,
        },
        "items": [],
        "puzzle": (
            'На пьедестале надпись: "Назовите число, которое идет после девяти". Введите ответ цифрой или словом.',  # noqa: E501
            ("10", "десять", "ten"),
            "treasure key",
        ),
    },
    TRAP_ROOM: {
        "description": 'Комната с хитрой плиточной поломкой. На стене видна надпись: "Осторожно — ловушка".',  # noqa: E501
        "exits": {"west": ENTRANCE, "east": LABORATORY},
        "items": ["rusty key"],
        "puzzle": (
            'Система плит активна. Чтобы пройти, назовите слово "шаг" три раза подряд (введите "шаг шаг шаг")',  # noqa: E501
            "шаг шаг шаг",
        ),
    },
    LIBRARY: {
        "description": "Пыльная библиотека. На полках старые свитки. Где-то здесь может быть ключ от сокровищницы.",  # noqa: E501
        "exits": {"east": HALL, "north": ARMORY},
        "items": ["ancient book"],
        "puzzle": (
            'В одном свитке загадка: "Что растет, когда его съедают?" (ответ одно слово)',  # noqa: E501
            "резонанс",
            "rusty key",
        ),
    },
    ARMORY: {
        "description": "Старая оружейная комната. На стене висит меч, рядом — небольшая бронзовая шкатулка.",  # noqa: E501
        "exits": {"south": LIBRARY},
        "items": ["sword", "bronze box"],
        "puzzle": None,
    },
    TREASURE_ROOM: {
        "description": "Комната, на столе большой сундук. Дверь заперта — нужен особый ключ.",  # noqa: E501
        "exits": {"south": HALL},
        "items": ["treasure chest"],
        "puzzle": (
            "Дверь защищена кодом. Введите код (подсказка: это число пятикратного шага, 2*5= ? ): ",  # noqa: E501
            ("10", "десять", "ten"),
        ),
    },
    LABORATORY: {
        "description": "Похоже, что это лаборатория. Везде расставлены пробирки и газовые горелки. На полке — записная книжка с пометками о реакциях.",  # noqa: E501
        "exits": {"west": TRAP_ROOM},
        "items": ["alchemist's notes"],
        "puzzle": (
            "Белый порошок в воде тает, пеною бурлит — кто я?",
            ("сода", "NaHCO3"),
        ),
    },
    STORAGE_ROOM: {
        "description": "Склад с бочками и ящиками разных размеров. Порывшись в них, вы, к сожалению, не находите ничего полезного.",  # noqa: E501
        "exits": {"west": HALL},
        "items": [],
        "puzzle": None,
    },
}

DEATH_TRAP_PROBABILITY = 30  # Вероятность смерти при попадании в ловушку, %
RANDOM_EVENT_PROBABILITY = 10  # Вероятность возникновения случайного события, %

COMMANDS = {
    "go <direction>": "перейти в направлении (north/south/east/west)",
    "look": "осмотреть текущую комнату",
    "take <item>": "поднять предмет",
    "use <item>": "использовать предмет из инвентаря",
    "inventory": "показать инвентарь",
    "solve": "попытаться решить загадку в комнате",
    "quit": "выйти из игры",
    "help": "показать это сообщение",
}
