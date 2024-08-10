from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime

from data.datatime import get_booked_intervals, get_available_slots, calculate_available_durations, \
    get_remaining_days_of_week, get_my_records

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Новая запись'), KeyboardButton(text='Мои записи')],
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


async def my_menu():
    from app.handlers import rec_plas
    my_men = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Редактировать', callback_data=f'rec_edit_{rec_plas}')],
            [InlineKeyboardButton(text='Отменить запись', callback_data=f'rec_cancellation_{rec_plas}')],
        ]
    )
    return my_men


async def days():
    keyboard = InlineKeyboardBuilder()
    available_days = get_remaining_days_of_week()
    for day in available_days:
        keyboard.add(InlineKeyboardButton(text=day, callback_data=day))
    return keyboard.adjust(1).as_markup()


async def durations():
    from app.handlers import s
    keyboards = InlineKeyboardBuilder()
    booked_intervals = get_booked_intervals(s['Place'], s['day'])
    start_time_user = datetime.strptime(s['time_start'], "%H:%M")
    available_durations = calculate_available_durations(start_time_user, booked_intervals)
    for duration in available_durations:
        keyboards.add(InlineKeyboardButton(text=f"{duration.seconds // 3600}:{(duration.seconds // 60) % 60:02}",
                                           callback_data=f"{duration.seconds // 3600}:{(duration.seconds // 60) % 60:02}"))
    return keyboards.adjust(2).as_markup()


async def available_slot():
    from app.handlers import s
    keyboard = InlineKeyboardBuilder()
    booked_intervals = get_booked_intervals(s['Place'], s['day'])
    available_slots = get_available_slots(booked_intervals)
    for slot in available_slots:
        keyboard.add(InlineKeyboardButton(text=slot.strftime('%H:%M'), callback_data=f'{slot.strftime('%H:%M')}'))
    return keyboard.adjust(2).as_markup()


async def get_rec():
    from app.handlers import user_named
    keyboard = InlineKeyboardBuilder()
    day = get_my_records(user_named)
    if 'У вас нет ни одной записи' in day[0]:
        keyboard.add(InlineKeyboardButton(text='У вас нет ни одной записи', callback_data=f'empty_rec'))
        return keyboard.adjust(1).as_markup()
    else:
        for d in day:
            keyboard.add(InlineKeyboardButton(text=f'Запись на {d[0]}, площадка - {d[1]}', callback_data=f'rec_{d[1]}'))
        return keyboard.adjust(1).as_markup()
