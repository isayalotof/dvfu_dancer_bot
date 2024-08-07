from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Новая запись'), KeyboardButton(text='Мой профиль')],
        [KeyboardButton(text='Информация')]
    ],
    resize_keyboard=True
)

place = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Place1', callback_data='Place1')],
        [InlineKeyboardButton(text='Place2', callback_data='Place2')],
        [InlineKeyboardButton(text='Place3', callback_data='Place3')],
        [InlineKeyboardButton(text='Place4', callback_data='Place4')],
    ]
)

time = ['10:00', '10:30',
        '10:00', '10:30',
        '10:00', '10:30',
        '10:00', '10:30',
        '10:00', '10:30',
        '10:00', '10:30',
        '10:00', '10:30',
        '10:00', '10:30',
        '10:00', '10:30',
        '10:00', '10:30',
        '10:00', '10:30',
        '10:00', '10:30',
        '10:00', '10:30',]

