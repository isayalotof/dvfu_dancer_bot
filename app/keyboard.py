from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from datetime import datetime, timedelta
from app import handlers
from data.data_base import c

from data.datatime import get_booked_intervals, get_available_slots, calculate_available_durations


main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Новая запись'), KeyboardButton(text='Мой профиль')],
        [KeyboardButton(text='Информация')]
    ],
    resize_keyboard=True
)


days = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Понедельник', callback_data='day_1')],
        [InlineKeyboardButton(text='Вторник', callback_data='day_2')],
        [InlineKeyboardButton(text='Среда', callback_data='day_3')],
        [InlineKeyboardButton(text='Четверг', callback_data='day_4')],
        [InlineKeyboardButton(text='Пятница', callback_data='day_5')],
        [InlineKeyboardButton(text='Суббота', callback_data='day_6')],
        [InlineKeyboardButton(text='Воскресенье', callback_data='day_7')],
    ]
)
place = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Place1', callback_data='Place1')],
        [InlineKeyboardButton(text='Place2', callback_data='Place2')],
        [InlineKeyboardButton(text='Place3', callback_data='Place3')],
        [InlineKeyboardButton(text='Place4', callback_data='Place4')],
    ]
)


async def durations():
    keyboards = InlineKeyboardBuilder()
    booked_intervals = get_booked_intervals('data.db', handlers.s['Place'], handlers.s['day'])
    start_time_user = datetime.strptime(handlers.s['time_start'], "%H:%M")
    available_durations = calculate_available_durations(start_time_user, booked_intervals)
    for duration in available_durations:
        keyboards.add(InlineKeyboardButton(text=f"{duration.seconds // 3600}:{(duration.seconds // 60) % 60:02}", callback_data=f"{duration.seconds // 3600}:{(duration.seconds // 60) % 60:02}"))
    return keyboards.adjust(2).as_markup()


async def available_slot():
    keyboard = InlineKeyboardBuilder()
    booked_intervals = get_booked_intervals('data.db', handlers.s['Place'], handlers.s['day'])
    available_slots = get_available_slots(booked_intervals)
    for slot in available_slots:
        keyboard.add(InlineKeyboardButton(text=slot.strftime('%H:%M'), callback_data=f'{slot.strftime('%H:%M')}'))
    return keyboard.adjust(2).as_markup()
