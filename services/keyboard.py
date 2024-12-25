from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_column_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [[KeyboardButton(text=item)] for item in items]
    return ReplyKeyboardMarkup(keyboard=row, resize_keyboard=True)


def make_keyboard_by_template(items: list[list[str]]) -> ReplyKeyboardMarkup:
    keyboard = []
    for row in items:
        keyboard.append([])
        for column in row:
            keyboard[-1].append(KeyboardButton(text=column))
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
