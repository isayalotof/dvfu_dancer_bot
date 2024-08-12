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


async def my_menu(rec_place):
    my_men = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Редактировать', callback_data=f'rec_edit_{rec_place}')],
            [InlineKeyboardButton(text='Отменить запись', callback_data=f'rec_cancellation_{rec_place}')],
        ]
    )
    return my_men


async def days():
    keyboard = InlineKeyboardBuilder()
    available_days = get_remaining_days_of_week()
    for day in available_days:
        keyboard.add(InlineKeyboardButton(text=day, callback_data=day))
    return keyboard.adjust(1).as_markup()


async def durations(dur_place, day, time_start):
    keyboards = InlineKeyboardBuilder()
    for duration in calculate_available_durations(datetime.strptime(time_start, "%H:%M"), get_booked_intervals(dur_place, day)):
        keyboards.add(InlineKeyboardButton(text=f"{duration.seconds // 3600}:{(duration.seconds // 60) % 60:02}",
                                           callback_data=f"{duration.seconds // 3600}:{(duration.seconds // 60) % 60:02}"))
    return keyboards.adjust(2).as_markup()


async def available_slot(av_place, day):
    keyboard = InlineKeyboardBuilder()
    for slot in get_available_slots(get_booked_intervals(av_place, day)):
        keyboard.add(InlineKeyboardButton(text=slot.strftime('%H:%M'), callback_data=f'{slot.strftime('%H:%M')}'))
    return keyboard.adjust(2).as_markup()


async def get_rec(username):
    keyboard = InlineKeyboardBuilder()
    day = get_my_records(username)
    if 'У вас нет ни одной записи' in day[0]:
        keyboard.add(InlineKeyboardButton(text='У вас нет ни одной записи', callback_data=f'empty_rec'))
        return keyboard.adjust(1).as_markup()
    else:
        for d in day:
            keyboard.add(InlineKeyboardButton(text=f'Запись на {d[0]}, площадка - {d[1]}', callback_data=f'rec_{d[1]}'))
        return keyboard.adjust(1).as_markup()
