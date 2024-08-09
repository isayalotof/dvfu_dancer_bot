from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from app import keyboard as kb, fsm
from aiogram.fsm.context import FSMContext
import sqlite3
from datetime import datetime, timedelta


db_path = "data.db"  # Путь к вашей базе данных
s = {}
db = sqlite3.connect('data.db')
c = db.cursor()
router = Router()
user_named = 0


@router.message(CommandStart())
async def cmd_start(message: Message):
    global user_named
    user_named = message.from_user.id
    await message.answer(f'Здравствуйте, {message.from_user.first_name}',
                        reply_markup=kb.main)
    if user_named in c.execute("""SELECT user_name FROM user""").fetchall():
        pass
    else:
        c.execute(f"""INSERT INTO user(user_name, Place1, Place2, Place3, Place4)
        VALUES('{message.from_user.id}', 1, 1, 1, 1)
        """)
        db.commit()


@router.message(F.text == 'Новая запись')
async def new_record(message: Message, state: FSMContext):
    global user_named
    user_named = message.from_user.id
    await state.set_state(fsm.Reg.username)
    await state.update_data(username=f"{message.from_user.id}")
    await state.set_state(fsm.Reg.place)
    await message.answer('Выберите площадку:', reply_markup=kb.place)


@router.callback_query(F.data == 'Place1')
async def set_place(callback: CallbackQuery, state: FSMContext):
    if 0 in c.execute(f"""SELECT Place1 FROM user WHERE user_name = {user_named};""").fetchone():
        await callback.message.edit_text('У вас не осталось записей на эту площадку\n'
                                         ' попробуйте выбрать другую или приходите в понедельник:',
                                         reply_markup=kb.place)
    else:
        await callback.answer('')
        await state.update_data(place='Place1')
        s['Place'] = 'Place1'
        await state.set_state(fsm.Reg.day)
        await callback.message.edit_text(f'Выберите день для записи: ', reply_markup=kb.days)


@router.callback_query(F.data == 'Place2')
async def set_place(callback: CallbackQuery, state: FSMContext):
    if 0 in c.execute(f"""SELECT Place2 FROM user WHERE user_name = {user_named};"""):
        await callback.message.edit_text('У вас не осталось записей на эту площадку\n'
                                         ' попробуйте выбрать другую или приходите в понедельник:', reply_markup=kb.place)
    else:
        await callback.answer('')
        await state.update_data(place='Place2')
        s['Place'] = 'Place2'
        await state.set_state(fsm.Reg.day)
        await callback.message.edit_text(f'Выберите день для записи: ', reply_markup=kb.days)


@router.callback_query(F.data == 'Place3')
async def set_place(callback: CallbackQuery, state: FSMContext):
    if 0 in c.execute(f"""SELECT Place3 FROM user WHERE user_name = {user_named};"""):
        await callback.message.edit_text('У вас не осталось записей на эту площадку\n'
                                         ' попробуйте выбрать другую или приходите в понедельник:', reply_markup=kb.place)
    else:
        await callback.answer('')
        await state.update_data(place='Place3')
        s['Place'] = 'Place3'
        await state.set_state(fsm.Reg.day)
        await callback.message.edit_text(f'Выберите день для записи: ', reply_markup=kb.days)


@router.callback_query(F.data == 'Place4')
async def set_place(callback: CallbackQuery, state: FSMContext):
    if 0 in c.execute(f"""SELECT Place4 FROM user WHERE user_name = {user_named};"""):
        await callback.message.edit_text('У вас не осталось записей на эту площадку\n'
                                         ' попробуйте выбрать другую или приходите в понедельник:', reply_markup=kb.place)
    else:
        await callback.answer('')
        await state.update_data(place='Place4')
        s['Place'] = 'Place4'
        await state.set_state(fsm.Reg.day)
        await callback.message.edit_text(f'Выберите день для записи: ', reply_markup=kb.days)


@router.callback_query(F.data == 'day_1')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(day='Monday')
    s['day'] = 'Monday'
    await state.set_state(fsm.Reg.time_start)
    await callback.message.edit_text('Выберите время начала', reply_markup=await kb.available_slot())


@router.callback_query(F.data == 'day_2')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(day='Tuesday')
    s['day'] = 'Tuesday'
    await state.set_state(fsm.Reg.time_start)
    await callback.message.edit_text('Выберите время начала', reply_markup=await kb.available_slot())


@router.callback_query(F.data == 'day_3')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(day='Wednesday')
    s['day'] = 'Wednesday'
    await state.set_state(fsm.Reg.time_start)
    await callback.message.edit_text('Выберите время начала', reply_markup=await kb.available_slot())


@router.callback_query(F.data == 'day_4')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(day='Thursday')
    s['day'] = 'Thursday'
    await state.set_state(fsm.Reg.time_start)
    await callback.message.edit_text('Выберите время начала', reply_markup=await kb.available_slot())


@router.callback_query(F.data == 'day_5')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(day='Friday')
    s['day'] = 'Friday'
    await state.set_state(fsm.Reg.time_start)
    await callback.message.edit_text('Выберите время начала', reply_markup=await kb.available_slot())


@router.callback_query(F.data == 'day_6')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(day='Saturday')
    s['day'] = 'Saturday'
    await state.set_state(fsm.Reg.time_start)
    await callback.message.edit_text('Выберите время начала', reply_markup=await kb.available_slot())


@router.callback_query(F.data == 'day_7')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(day='Sunday')
    s['day'] = 'Sunday'
    await state.set_state(fsm.Reg.time_start)
    await callback.message.edit_text('Выберите время начала', reply_markup=await kb.available_slot())


@router.callback_query(F.data == '10:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='10:00')
    s['time_start'] = '10:00'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберете длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '10:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='10:30')
    s['time_start'] = '10:30'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберете длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '11:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='11:00')
    s['time_start'] = '11:00'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберете длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '11:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='11:30')
    s['time_start'] = '11:30'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберете длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '12:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='12:00')
    s['time_start'] = '12:00'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберете длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '12:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='12:30')
    s['time_start'] = '12:30'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберете длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '13:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='13:00')
    s['time_start'] = '13:00'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберете длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '13:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='13:30')
    s['time_start'] = '13:30'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберете длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '14:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='14:00')
    s['time_start'] = '14:00'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберете длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '14:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='14:30')
    s['time_start'] = '14:30'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберете длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '15:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='15:00')
    s['time_start'] = '15:00'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберете длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '15:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='15:30')
    s['time_start'] = '15:30'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберете длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '16:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='16:00')
    s['time_start'] = '16:00'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберете длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '16:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='16:30')
    s['time_start'] = '16:30'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберете длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '17:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='17:00')
    s['time_start'] = '17:00'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберете длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '17:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='17:30')
    s['time_start'] = '17:30'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберете длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '18:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='18:00')
    s['time_start'] = '18:00'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберете длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '18:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='18:30')
    s['time_start'] = '18:30'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберете длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '19:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='19:00')
    s['time_start'] = '19:00'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберете длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '19:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='19:30')
    s['time_start'] = '19:30'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберете длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '20:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='20:00')
    s['time_start'] = '20:00'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберете длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '20:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='20:30')
    s['time_start'] = '20:30'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберете длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '21:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='21:00')
    s['time_start'] = '21:00'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберете длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '21:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='21:30')
    s['time_start'] = '21:30'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберете длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '0:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(duration=0.5)
    await state.set_state(fsm.Reg.people_group)
    await callback.message.edit_text("Отправьте одним сообщением ФИО всех людей,\n которые прийдут по этой записи: ")


@router.callback_query(F.data == '1:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(duration=1.0)
    await state.set_state(fsm.Reg.people_group)
    await callback.message.edit_text("Отправьте одним сообщением ФИО всех людей,\n которые прийдут по этой записи: ")


@router.callback_query(F.data == '1:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(duration=1.5)
    await state.set_state(fsm.Reg.people_group)
    await callback.message.edit_text("Отправьте одним сообщением ФИО всех людей,\n которые прийдут по этой записи: ")


@router.callback_query(F.data == '2:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(duration=2.0)
    await state.set_state(fsm.Reg.people_group)
    await callback.message.edit_text("Отправьте одним сообщением ФИО всех людей,\n которые прийдут по этой записи: ")


@router.callback_query(F.data == '2:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(duration=2.5)
    await state.set_state(fsm.Reg.people_group)
    await callback.message.edit_text("Отправьте одним сообщением ФИО всех людей,\n которые прийдут по этой записи: ")


@router.callback_query(F.data == '3:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(duration=3.0)
    await state.set_state(fsm.Reg.people_group)
    await callback.message.edit_text("""Отправьте одним сообщением ФИО всех людей,\n
            которые прийдут по этой записи:\n
            обратите внимание что список людей нужно указать в формате\n
            Наша Группа:\n
            1)...\n
            2)...\n
            .)...
            """)


@router.message()
async def empty_handler(message: Message, state: FSMContext):
    if '1' in message.text and ')' in message.text:
        await state.update_data(people_group=f'{message.text}')
        data = await state.get_data()
        table_name = data['place']
        c.execute(f"""
            INSERT INTO {table_name} (username, day, time_start, duration, people_group)
            VALUES (?, ?, ?, ?, ?);
        """, (data['username'], data['day'], data['time_start'], data['duration'], data['people_group']))
        db.commit()
        c.execute(f"""UPDATE user
        SET {table_name} = 0 WHERE user_name = {user_named};""")
        db.commit()
        await message.answer('Запись успешно добавлена')
    else:
        await message.answer('Наверное я вас не так понял, проверьте правильность сообщения')
        await message.answer_sticker('CAACAgIAAxkBAAEMoJ9mtlZLkbGXWas11BUXexN-I1WChgAC1UkAAtOjkUux-DPRTXoxATUE')



