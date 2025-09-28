from math import floor, sin

from .constants import (
    CURRENT_ROOM,
    DEATH_TRAP_PROBABILITY,
    DESCRIPTION,
    EXITS,
    GAME_OVER,
    ITEMS,
    PLAYER_INVENTORY,
    PUZZLE,
    RANDOM_EVENT_PROBABILITY,
    ROOMS,
    STEPS_TAKEN,
    TRAP_ROOM,
)


def describe_current_room(game_state: dict):
    """
    Выводит подробное описание комнаты, в которой находится игрок.

    Args:
        game_state (dict): Текущее состояние игры.
    """

    current_room = game_state[CURRENT_ROOM]
    room_data = get_room_data(current_room)

    room_name = current_room.replace("_", " ").upper()
    print(f"== {room_name} ==")
    print(room_data[DESCRIPTION])

    if items := room_data[ITEMS]:
        print(f"Заметные предметы: {', '.join(items)}")

    exits = room_data[EXITS].keys()
    print(f"Выходы: {', '.join(exits)}")

    if room_data[PUZZLE]:
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


def challenge_player(puzzle: tuple) -> str | None:
    """
    Загадывает игроку загадку и проверяет его ответ. Если ответ верный, возвращает
    строку с названием предмета, который получен в качестве награды.

    Args:
        puzzle (tuple): Загадка, правильный ответ и опциональная награда
        (кортеж из 2 или 3 значений).
    Returns:
        str | None: Предмет-награда или None, если загадка не была решена.
    """

    question, answer = puzzle[:2]
    reward = puzzle[2] if len(puzzle) > 2 else "valuable coin"

    print(question)
    user_input = input("Ваш ответ: ").strip()

    if hasattr(answer, "__iter__") and not isinstance(answer, str):
        correct = user_input in answer
    else:
        correct = user_input == answer

    if correct:
        return reward


def solve_puzzle(game_state: dict):
    """
    Пытается решить загадку, выводя её текст и проверяя полученный
    от игрока ответ. Если загадка решена, то добавляет игроку награду.

    Args:
        game_state (dict): Текущее состояние игры.
    """

    current_room = game_state[CURRENT_ROOM]
    room_data = get_room_data(current_room)

    if not (puzzle := room_data[PUZZLE]):
        print("Загадок здесь нет.")
        return

    if reward := challenge_player(puzzle):
        print(f"Вы успешно решили загадку и получаете награду: {reward}")
        game_state[PLAYER_INVENTORY].append(reward)
        room_data[PUZZLE] = None
    else:
        print("Неверно. Попробуйте снова.")
        if current_room == TRAP_ROOM:
            trigger_trap(game_state)


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
        room_data[ITEMS].remove(treasure_chest)
        print("В сундуке сокровище! Вы победили!")
        game_state[GAME_OVER] = True

    room_data = get_room_data(game_state[CURRENT_ROOM])
    room_items = room_data[ITEMS]

    if treasure_chest not in room_items:
        print("Сундук уже открыт или отсутствует.")
        return

    if "treasure key" in game_state[PLAYER_INVENTORY]:
        open_chest(
            game_state,
            room_data,
            "Вы применяете ключ, и замок щёлкает. Сундук открыт!",
        )
    elif input("Сундук заперт. ... Ввести код? (да/нет) ").strip() == "да":
        if challenge_player(room_data[PUZZLE]):
            open_chest(
                game_state,
                room_data,
                "Вы ввели верный код, и замок щёлкает. Сундук открыт!",
            )
        else:
            print("Похоже, что код неверный.")
    else:
        print("Вы отступаете от сундука.")


def show_help(commands: dict):
    """
    Выводит доступные пользователю команды.

    Args:
        commands (dict): словарь команд (команда -> описание).
    """

    print("\nДоступные команды:")
    for command, description in commands.items():
        print(f"  {command:<16}- {description}")


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

    inventory = game_state[PLAYER_INVENTORY]
    seed = game_state[STEPS_TAKEN]

    if inventory:
        index = pseudo_random(seed, len(inventory))
        item_lost = inventory.pop(index)
        print(f"Вам удаётся избежать ловушки, но вы теряете {item_lost}")
    elif pseudo_random(seed, 100) < DEATH_TRAP_PROBABILITY:
        print("Вам не удаётся избежать ловушки, и вы погибаете. Поражение!")
        game_state[GAME_OVER] = True
    else:
        print("Вам чудом удалось избежать смертельной ловушки.")


def random_event(game_state: dict):
    """
    Выполняет действия, которые происходят при случайном событии.

    Args:
        game_state (dict): Текущее состояние игры.
    """

    seed = game_state[STEPS_TAKEN]

    if pseudo_random(seed, 100) < RANDOM_EVENT_PROBABILITY:
        inventory = game_state[PLAYER_INVENTORY]

        match pseudo_random(seed, 3):
            case 0:
                print("Удача! Вы увидели на полу комнаты монетку.")
                coin = "coin"
                room_data = get_room_data(game_state[CURRENT_ROOM])
                room_data[ITEMS].append(coin)
            case 1:
                print("Вы слышите какой-то шорох.")
                if "sword" in inventory:
                    print("Вы хватаетесь за меч и отпугиваете монстра.")
            case 2:
                in_trap_room = game_state[CURRENT_ROOM] == TRAP_ROOM
                no_torch = "torch" not in inventory
                if in_trap_room and no_torch:
                    print("Вы чувствуете опасность.")
                    trigger_trap(game_state)
