#!/usr/bin/env python3

from sys import exit

from .player_actions import get_input, move_player, show_inventory, take_item, use_item
from .utils import describe_current_room

game_state = {
    "player_inventory": [],  # Инвентарь игрока
    "current_room": "entrance",  # Текущая комната
    "game_over": False,  # Значения окончания игры
    "steps_taken": 0,  # Количество шагов
}


def process_command(game_state: dict, command: str):
    """
    Обрабатывает введённую пользователем команду.
    Доступные команды: look, use, go, take, inventory, quit | exit

    Args:
        game_state (dict): Текущее состояние игры.
        command (str): Команда, полученная от пользователя.
    """

    parts = [part.strip() for part in command.split(" ", maxsplit=1)]

    if len(parts) == 1:
        cmd, arg = parts[0], ""
    else:
        cmd, arg = parts

    match cmd:
        case "look":
            describe_current_room(game_state)
        case "use":
            use_item(game_state, arg)
        case "go":
            move_player(game_state, arg)
        case "take":
            take_item(game_state, arg)
        case "inventory":
            show_inventory(game_state)
        case "quit" | "exit":
            print("\nВыход из игры.")
            exit(0)


def main():
    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while True:
        command = get_input()
        process_command(game_state, command)


if __name__ == "__main__":
    main()
