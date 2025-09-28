#!/usr/bin/env python3

from sys import exit

from .constants import (
    COMMANDS,
    CURRENT_ROOM,
    ENTRANCE,
    GAME_OVER,
    PLAYER_INVENTORY,
    STEPS_TAKEN,
    TREASURE_ROOM,
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
    arg_is_treasure = arg == "treasure chest"

    match cmd:
        case "look":
            describe_current_room(game_state)
        case "use":
            if in_treasure_room and arg_is_treasure:
                attempt_open_treasure(game_state)
            else:
                use_item(game_state, arg)
        case "go" | "north" | "south" | "west" | "east":
            direction = arg if cmd == "go" else cmd
            move_player(game_state, direction)
        case "take":
            if in_treasure_room and arg_is_treasure:
                print("Сундук с сокровищами слишком большой, чтобы его поднять.")
            else:
                take_item(game_state, arg)
        case "inventory":
            show_inventory(game_state)
        case "solve":
            if in_treasure_room:
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case "quit" | "exit":
            print("\nВыход из игры.")
            exit(0)
        case "help":
            show_help(COMMANDS)


def main():
    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state[GAME_OVER]:
        command = get_input()
        process_command(game_state, command)


if __name__ == "__main__":
    main()
