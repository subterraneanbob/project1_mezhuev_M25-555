#!/usr/bin/env python3

from sys import exit

from .constants import (
    COMMANDS,
    CURRENT_ROOM,
    DIRECTIONS,
    ENTRANCE,
    EXIT,
    GAME_OVER,
    GO,
    HELP,
    INVENTORY,
    LOOK,
    PLAYER_INVENTORY,
    QUIT,
    SOLVE,
    STEPS_TAKEN,
    TAKE,
    TREASURE_CHEST,
    TREASURE_ROOM,
    USE,
)
from .player_actions import get_input, move_player, show_inventory, take_item, use_item
from .utils import attempt_open_treasure, describe_current_room, show_help, solve_puzzle

game_state = {
    PLAYER_INVENTORY: [],  # Инвентарь игрока
    CURRENT_ROOM: ENTRANCE,  # Текущая комната
    GAME_OVER: False,  # Значения окончания игры
    STEPS_TAKEN: 0,  # Количество шагов
}


def process_command(game_state: dict, command: str):
    """
    Обрабатывает введённую пользователем команду.
    Доступные команды: look, use, go, take, inventory, solve, quit | exit

    Args:
        game_state (dict): Текущее состояние игры.
        command (str): Команда, полученная от пользователя.
    """

    parts = [part.strip() for part in command.split(" ", maxsplit=1)]

    if len(parts) == 1:
        cmd, arg = parts[0], ""
    else:
        cmd, arg = parts

    in_treasure_room = game_state[CURRENT_ROOM] == TREASURE_ROOM
    arg_is_treasure = arg == TREASURE_CHEST

    if cmd == LOOK:
        describe_current_room(game_state)
    elif cmd == USE:
        if in_treasure_room and arg_is_treasure:
            attempt_open_treasure(game_state)
        else:
            use_item(game_state, arg)
    elif cmd == GO:
        move_player(game_state, arg)
    elif cmd in DIRECTIONS:
        move_player(game_state, cmd)
    elif cmd == TAKE:
        if in_treasure_room and arg_is_treasure:
            print("Сундук с сокровищами слишком большой, чтобы его поднять.")
        else:
            take_item(game_state, arg)
    elif cmd == INVENTORY:
        show_inventory(game_state)
    elif cmd == SOLVE:
        if in_treasure_room:
            attempt_open_treasure(game_state)
        else:
            solve_puzzle(game_state)
    elif cmd == QUIT or cmd == EXIT:
        print("\nВыход из игры.")
        exit(0)
    elif cmd == HELP:
        show_help(COMMANDS)


def main():
    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state[GAME_OVER]:
        command = get_input()
        process_command(game_state, command)


if __name__ == "__main__":
    main()
