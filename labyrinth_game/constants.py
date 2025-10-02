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

# Атрибуты комнаты
DESCRIPTION = "description"
EXITS = "exits"
ITEMS = "items"
PUZZLE = "puzzle"

# Направления движения
NORTH = "north"
SOUTH = "south"
WEST = "west"
EAST = "east"
DIRECTIONS = (NORTH, SOUTH, WEST, EAST)

# Ключевые предметы
TORCH = "torch"
TREASURE_KEY = "treasure key"  # Открывает сундук с сокровищами
RUSTY_KEY = "rusty key"  # Открывает дверь к сокровищам
SWORD = "sword"
BRONZE_BOX = "bronze box"
TREASURE_CHEST = "treasure chest"
COIN = "coin"
VALUABLE_COIN = "valuable coin"  # Награда по-умолчанию, если не указана явно


ROOMS = {
    ENTRANCE: {
        DESCRIPTION: "Вы в темном входе лабиринта...",
        EXITS: {NORTH: HALL, EAST: TRAP_ROOM},
        ITEMS: [TORCH],
        PUZZLE: None,
    },
    HALL: {
        DESCRIPTION: "Большой зал с эхом. По центру стоит пьедестал с запечатанным сундуком.",  # noqa: E501
        EXITS: {
            SOUTH: ENTRANCE,
            WEST: LIBRARY,
            NORTH: TREASURE_ROOM,
            EAST: STORAGE_ROOM,
        },
        ITEMS: [],
        PUZZLE: (
            'На пьедестале надпись: "Назовите число, которое идет после девяти". Введите ответ цифрой или словом.',  # noqa: E501
            ("10", "десять", "ten"),
            TREASURE_KEY,
        ),
    },
    TRAP_ROOM: {
        DESCRIPTION: 'Комната с хитрой плиточной поломкой. На стене видна надпись: "Осторожно — ловушка".',  # noqa: E501
        EXITS: {WEST: ENTRANCE, EAST: LABORATORY},
        ITEMS: [RUSTY_KEY],
        PUZZLE: (
            'Система плит активна. Чтобы пройти, назовите слово "шаг" три раза подряд (введите "шаг шаг шаг")',  # noqa: E501
            "шаг шаг шаг",
        ),
    },
    LIBRARY: {
        DESCRIPTION: "Пыльная библиотека. На полках старые свитки. Где-то здесь может быть ключ от сокровищницы.",  # noqa: E501
        EXITS: {EAST: HALL, NORTH: ARMORY},
        ITEMS: ["ancient book"],
        PUZZLE: (
            'В одном свитке загадка: "Что растет, когда его съедают?" (ответ одно слово)',  # noqa: E501
            "резонанс",
            RUSTY_KEY,
        ),
    },
    ARMORY: {
        DESCRIPTION: "Старая оружейная комната. На стене висит меч, рядом — небольшая бронзовая шкатулка.",  # noqa: E501
        EXITS: {SOUTH: LIBRARY},
        ITEMS: [SWORD, BRONZE_BOX],
        PUZZLE: None,
    },
    TREASURE_ROOM: {
        DESCRIPTION: "Комната, на столе большой сундук. Дверь заперта — нужен особый ключ.",  # noqa: E501
        EXITS: {SOUTH: HALL},
        ITEMS: [TREASURE_CHEST],
        PUZZLE: (
            "Дверь защищена кодом. Введите код (подсказка: это число пятикратного шага, 2*5= ? ): ",  # noqa: E501
            ("10", "десять", "ten"),
        ),
    },
    LABORATORY: {
        DESCRIPTION: "Похоже, что это лаборатория. Везде расставлены пробирки и газовые горелки. На полке — записная книжка с пометками о реакциях.",  # noqa: E501
        EXITS: {WEST: TRAP_ROOM},
        ITEMS: ["alchemist's notes"],
        PUZZLE: (
            "Белый порошок в воде тает, пеною бурлит — кто я?",
            ("сода", "NaHCO3"),
        ),
    },
    STORAGE_ROOM: {
        DESCRIPTION: "Склад с бочками и ящиками разных размеров. Порывшись в них, вы, к сожалению, не находите ничего полезного.",  # noqa: E501
        EXITS: {WEST: HALL},
        ITEMS: [],
        PUZZLE: None,
    },
}

DEATH_TRAP_PROBABILITY = 30  # Вероятность смерти при попадании в ловушку, %
RANDOM_EVENT_PROBABILITY = 10  # Вероятность возникновения случайного события, %

# Команды
GO = "go"
LOOK = "look"
TAKE = "take"
USE = "use"
INVENTORY = "inventory"
SOLVE = "solve"
QUIT = "quit"
EXIT = "exit"
HELP = "help"

COMMANDS = {
    f"{GO} <direction>": "перейти в направлении (north/south/east/west)",
    LOOK: "осмотреть текущую комнату",
    f"{TAKE} <item>": "поднять предмет",
    f"{USE} <item>": "использовать предмет из инвентаря",
    INVENTORY: "показать инвентарь",
    SOLVE: "попытаться решить загадку в комнате",
    QUIT: "выйти из игры",
    HELP: "показать это сообщение",
}
