from math import floor, sin

from .constants import DEATH_TRAP_PROBABILITY, ROOMS


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


def attempt_open_treasure(game_state: dict):
    """
    Пытается открыть сундук с сокровищами, проверяя наличие ключа у игрока или
    загадывая ему загадку. Если игрок успешно справился, то игра завершается.

    Args:
        game_state (dict): Текущее состояние игры.
    """
    treasure_chest = "treasure chest"

    def open_chest(game_state: dict, room_data: dict, message: str):
        print(message)
        room_data["items"].remove(treasure_chest)
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True

    room_data = get_room_data(game_state["current_room"])
    room_items = room_data["items"]

    if treasure_chest not in room_items:
        print("Сундук уже открыт или отсутствует.")
        return

    inventory = game_state["player_inventory"]
    keys = ["treasure key", "rusty key"]

    if any(k in inventory for k in keys):
        open_chest(
            game_state,
            room_data,
            "Вы применяете ключ, и замок щёлкает. Сундук открыт!",
        )
    elif input("Сундук заперт. ... Ввести код? (да/нет) ").strip() == "да":
        question, answer = room_data["puzzle"]
        if input(question).strip() == answer:
            open_chest(
                game_state,
                room_data,
                "Вы ввели верный код, и замок щёлкает. Сундук открыт!",
            )
        else:
            print("Похоже, что код неверный.")
    else:
        print("Вы отступаете от сундука.")


def show_help():
    """
    Выводит доступные пользователю команды.
    """

    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")


def pseudo_random(seed: int, modulo: int) -> int:
    """
    Возвращает псевдо-случайное целое число в диапазоне [0; modulo),
    используя заданное зерно случайности seed.

    Args:
        seed (int): Зерно случайности.
        modulo (int): Число для определения диапазона.
    Returns:
        int: Псевдо-случайное число.
    """

    # Вычисляем псевдо-случайное число
    random_number = sin(seed * 12.9898) * 43758.5453

    # Оставляем только дробную часть
    fraction = random_number - floor(random_number)

    # Приводим к требуемому диапазону и отбрасываем дробную часть
    return int(fraction * modulo)


def trigger_trap(game_state: dict):
    """
    Выполняет действия при срабатывании ловушки. Если у игрока есть предметы
    в инвентаре, то он теряет один случайный предмет. В противном случае
    есть шанс, что игрок погибнет, и игра завершится.

    Args:
        game_state (dict): Текущее состояние игры.
    """

    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state["player_inventory"]
    seed = game_state["steps_taken"]

    if inventory:
        index = pseudo_random(seed, len(inventory))
        item_lost = inventory.pop(index)
        print(f"Вам удаётся избежать ловушки, но вы теряете {item_lost}")
    elif pseudo_random(seed, 100) < DEATH_TRAP_PROBABILITY:
        print("Вам не удаётся избежать ловушки, и вы погибаете. Поражение!")
        game_state["game_over"] = True
    else:
        print("Вам чудом удалось избежать смертельной ловушки.")
