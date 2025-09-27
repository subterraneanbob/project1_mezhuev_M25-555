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
