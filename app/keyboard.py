from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime

from data.datatime import get_booked_intervals, get_available_slots, calculate_available_durations, \
    get_remaining_days_of_week, get_my_records, get_eng_day, calculate_duration

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Новая запись'), KeyboardButton(text='Мои записи')],
        [KeyboardButton(text='Информация')]
    ],
    resize_keyboard=True
)

place = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Place1', callback_data='Place_Place1')],
        [InlineKeyboardButton(text='Place2', callback_data='Place_Place2')],
        [InlineKeyboardButton(text='Place3', callback_data='Place_Place3')],
        [InlineKeyboardButton(text='Place4', callback_data='Place_Place4')],
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
    for day in get_remaining_days_of_week():
        keyboard.add(InlineKeyboardButton(text=day, callback_data=f'day_{get_eng_day(day)}'))
    return keyboard.adjust(1).as_markup()


async def durations(dur_place, day, time_start):
    keyboards = InlineKeyboardBuilder()
    for duration in calculate_available_durations(datetime.strptime(time_start, "%H:%M"), get_booked_intervals(dur_place, day)):
        keyboards.add(InlineKeyboardButton(text=f"{duration.seconds // 3600}:{(duration.seconds // 60) % 60:02}",
                                           callback_data=f"av_slot_{calculate_duration(duration)}"))
    return keyboards.adjust(2).as_markup()


async def available_slot(av_place, day):
    keyboard = InlineKeyboardBuilder()
    for slot in get_available_slots(get_booked_intervals(av_place, day)):
        keyboard.add(InlineKeyboardButton(text=slot.strftime('%H:%M'), callback_data=f'time_start_{slot.strftime('%H:%M')}'))
    return keyboard.adjust(2).as_markup()


async def get_rec(username):
    keyboard = InlineKeyboardBuilder()
    day = get_my_records(username)
    if 'У вас нет ни одной записи' in day[0]:
        keyboard.add(InlineKeyboardButton(text='У вас нет ни одной записи', callback_data=f'empty_rec'))
    else:
        for d in day:
            keyboard.add(InlineKeyboardButton(text=f'Запись на {d[0]}, площадка - {d[1]}', callback_data=f'rect_{d[1]}'))
    return keyboard.adjust(1).as_markup()
