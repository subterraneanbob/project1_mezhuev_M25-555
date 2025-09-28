from .constants import (
    BRONZE_BOX,
    CURRENT_ROOM,
    EXITS,
    ITEMS,
    PLAYER_INVENTORY,
    RUSTY_KEY,
    STEPS_TAKEN,
    SWORD,
    TORCH,
    TREASURE_ROOM,
)
from .utils import describe_current_room, get_room_data, random_event


def show_inventory(game_state: dict):
    """
    Выводит предметы в инвентаре или сообщение, что инвентарь пуст.

    Args:
        game_state (dict): Текущее состояние игры.
    """

    if inventory := game_state[PLAYER_INVENTORY]:
        print(f"Инвентарь: {', '.join(inventory)}")
    else:
        print("Инвентарь пуст.")


def get_input(prompt="> ") -> str:
    """
    Запрашивает у пользователя команду и возвращает её.

    Args:
        prompt (object): приглашение пользователя к вводу
    """

    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print()
        return "quit"


def move_player(game_state: dict, direction: str):
    """
    Перемещает игрока в заданном направлении, если есть возможность.
    Обновляет состояние игры (текущая комната, количество шагов) и выводит
    описание новой комнаты.

    Args:
        game_state (dict): Текущее состояние игры.
        direction (str): Направление движения.
    """

    room_data = get_room_data(game_state[CURRENT_ROOM])
    exits = room_data[EXITS]

    if direction in exits:
        if (next_room := exits[direction]) == TREASURE_ROOM:
            inventory = game_state[PLAYER_INVENTORY]
            if RUSTY_KEY in inventory:
                print(
                    "Вы используете найденный ключ, чтобы открыть путь в "
                    "комнату сокровищ."
                )
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return  # Не переходим в след. комнату

        game_state[CURRENT_ROOM] = next_room
        game_state[STEPS_TAKEN] += 1
        describe_current_room(game_state)
        random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state: dict, item_name: str):
    """
    Добавляет предмет в инвентарь игрока, если он есть в комнате.
    Выводит сообщение о результате в любом случае, даже если предмета нет.

    Args:
        game_state (dict): Текущее состояние игры.
        item_name (str): Название предмета.
    """

    room_data = get_room_data(game_state[CURRENT_ROOM])
    room_items = room_data[ITEMS]

    if item_name in room_items:
        game_state[PLAYER_INVENTORY].append(item_name)
        room_items.remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state: dict, item_name: str):
    """
    Использует предмет, если он есть у игрока. Эффект зависит от предмета.

    Args:
        game_state (dict): Текущее состояние игры.
        item_name (str): Название предмета.
    """

    available_items = game_state[PLAYER_INVENTORY]

    if item_name not in available_items:
        print("У вас нет такого предмета.")
        return

    match item_name:
        case _ if item_name == TORCH:
            print("Вы зажигаете факел, и становится светлее.")
        case _ if item_name == SWORD:
            print("Вы сжимаете меч в руке, и это добавляет вам уверенности.")
        case _ if item_name == BRONZE_BOX:
            if RUSTY_KEY in available_items:
                print("Коробка пуста.")
            else:
                print("Вы открываете шкатулку и достаёте оттуда ржавый ключ.")
                available_items.append(RUSTY_KEY)
        case _:
            print("Вы не знаете, как использовать этот предмет.")
