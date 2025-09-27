from .constants import ROOMS


def describe_current_room(game_state: dict):
    """
    Выводит подробное описание комнаты, в которой находится игрок.

    Args:
        game_state (dict): Текущее состояние игры.
    """

    current_room = game_state["current_room"]
    room_data = get_room_data(current_room)

    room_name = current_room.replace("_", " ").upper()
    print(f"== {room_name} ==")
    print(room_data["description"])

    if items := room_data["items"]:
        print(f"Заметные предметы: {', '.join(items)}")

    exits = room_data["exits"].keys()
    print(f"Выходы: {', '.join(exits)}")

    if room_data["puzzle"]:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def get_room_data(room_name: str) -> dict:
    """
    Возвращает данные комнаты по её названию или пустой словарь, если комната
    не найдена.

    Args:
        room_name (str): Название комнаты.
    Returns:
        dict: Данные комнаты.
    """

    return ROOMS[room_name] if room_name in ROOMS else {}


def solve_puzzle(game_state: dict):
    """
    Пытается решить загадку, выводя её текст и проверяя полученный
    от игрока ответ. Если загадка решена, то добавляет игроку награду.

    Args:
        game_state (dict): Текущее состояние игры.
    """

    room_data = get_room_data(game_state["current_room"])

    if not (puzzle := room_data["puzzle"]):
        print("Загадок здесь нет.")
        return

    puzzle_text, answer = puzzle
    print(puzzle_text)

    if input("Ваш ответ: ").strip() == answer:
        print("Вы успешно решили загадку и получаете награду.")
        game_state["player_inventory"].append("valuable coin")
        room_data["puzzle"] = None
    else:
        print("Неверно. Попробуйте снова.")
