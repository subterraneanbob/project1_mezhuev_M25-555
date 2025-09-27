from .utils import describe_current_room, get_room_data


def show_inventory(game_state: dict):
    """
    Выводит предметы в инвентаре или сообщение, что инвентарь пуст.

    Args:
        game_state (dict): Текущее состояние игры.
    """

    if inventory := game_state["player_inventory"]:
        print(f"Инвентарь: {', '.join(inventory)}")
    else:
        print("Инвентарь пуст.")


def get_input(prompt="> ") -> str:
    """
    Запрашивает у пользователя данные (команду, название, ответ) и возвращает их.

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

    room_data = get_room_data(game_state["current_room"])
    exits = room_data["exits"]

    if direction in exits:
        game_state["current_room"] = exits[direction]
        game_state["steps_taken"] += 1
        describe_current_room(game_state)
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

    room_data = get_room_data(game_state["current_room"])
    room_items = room_data["items"]

    if item_name in room_items:
        game_state["player_inventory"].append(item_name)
        room_items.remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")
