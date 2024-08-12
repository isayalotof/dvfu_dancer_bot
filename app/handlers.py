from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from app import keyboard as kb, fsm
from aiogram.fsm.context import FSMContext
from main import bot
from data.datatime import get_date_of_weekday
from data.data_base import c, db

db_path = "data.db"

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Здравствуйте, {message.from_user.first_name.capitalize()} ',
                         reply_markup=kb.main)
    if c.execute("SELECT COUNT(*) FROM user WHERE user_name = ?", (message.from_user.id,)).fetchone()[0]:
        pass
    else:
        c.execute(
            """INSERT INTO user(user_name, Place1, Place2, Place3, Place4)
               VALUES(?, 1, 1, 1, 1)
            """,
            (message.from_user.id,))
        db.commit()


@router.message(F.text == 'Новая запись')
async def new_record(message: Message, state: FSMContext):
    if c.execute("SELECT COUNT(*) FROM user WHERE user_name = ?", (message.from_user.id,)).fetchone()[0]:
        pass
    else:
        c.execute(
            """INSERT INTO user(user_name, Place1, Place2, Place3, Place4)
               VALUES(?, 1, 1, 1, 1)
            """,
            (message.from_user.id,))
        db.commit()
    await state.set_state(fsm.Registration.username)
    await state.update_data(username=f"{message.from_user.id}")
    await state.set_state(fsm.Registration.place)
    await message.answer('Выберите площадку:', reply_markup=kb.place)


@router.message(F.text == 'Мои записи')
async def new_record(message: Message):
    if c.execute("SELECT COUNT(*) FROM user WHERE user_name = ?", (message.from_user.id,)).fetchone()[0]:
        pass
    else:
        c.execute(
            """INSERT INTO user(user_name, Place1, Place2, Place3, Place4)
               VALUES(?, 1, 1, 1, 1)
            """,
            (message.from_user.id,))
        db.commit()
    await message.answer('Ваши записи:', reply_markup=await kb.get_rec(message.from_user.id))


@router.message(F.text == 'Информация')
async def my_info(message: Message):
    await message.answer("Информация, когда мне датут тг админа я прифигачу сюда его контакты, а пока хз")


@router.callback_query(F.data.startswith('Place_'))
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    if 0 in [row[0] for row in
             c.execute(f"SELECT {callback.data.replace('Place_', '')} FROM user WHERE user_name = ?", (callback.from_user.id,)).fetchall()]:
        await callback.message.edit_text(
            'У вас не осталось записей на эту площадку\n'
            'попробуйте выбрать другую или приходите позже:',
            reply_markup=kb.place
        )
    else:
        await state.update_data(place=f'{callback.data.replace('Place_', '')}')
        await state.set_state(fsm.Registration.day)
        await callback.message.edit_text(f'Выберите день для записи: ', reply_markup=await kb.days())


@router.callback_query(F.data.startswith('day_'))
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(day=f'{callback.data.replace('day_', '')}')
    data = await state.get_data()
    await state.set_state(fsm.Registration.time_start)
    await callback.message.edit_text('Выберите время начала',
                                     reply_markup=await kb.available_slot(data['place'], data['day']))


@router.callback_query(F.data.startswith('time_start_'))
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start=f'{callback.data.replace('time_start_', '')}')
    data = await state.get_data()
    await state.set_state(fsm.Registration.duration)
    await callback.message.edit_text("Выберите длительность: ",
                                     reply_markup=await kb.durations(data['place'], data['day'], data['time_start']))


@router.callback_query(F.data.startswith('av_slot_'))
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(duration=float(callback.data.replace('av_slot_', '')))
    await state.set_state(fsm.Registration.people_group)
    await callback.message.edit_text(f"Отправьте ФИО всех кто придет по этой записи\n"
                                     f"Обратите внимание,\n"
                                     f"Все люди должны быть указанны и пронумерованны\n"
                                     f"Пример:\n"
                                     f"1) Гуманоид 1\n"
                                     f"2) Гуманоид 2\n"
                                     f"и тд \n")


@router.callback_query(F.data.startswith('rect_'))
async def my_rec_place(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(f"Запись на {callback.data.replace('rect_','')}, что хотите сделать?", reply_markup=await kb.my_menu(callback.data.replace('rect_','')))


@router.callback_query(F.data.startswith('rec_edit_'))
async def edit_rec(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await bot.delete_message(chat_id='-1002186891939', message_id=int(
        c.execute(f"""SELECT mesage_id FROM {callback.data.replace('rec_edit_', '')} WHERE username = {str(callback.from_user.id)}""").fetchall()[0][0]))
    c.execute(f"""DELETE FROM {callback.data.replace('rec_edit_', '')} WHERE username = {callback.from_user.id}""")
    db.commit()
    await state.set_state(fsm.Registration.username)
    await state.update_data(username=f"{callback.from_user.id}")
    await state.set_state(fsm.Registration.place)
    await state.update_data(place=f'{callback.data.replace('rec_edit_', '')}')
    await state.set_state(fsm.Registration.day)
    await callback.message.edit_text(f'Выберите день для записи: ', reply_markup=await kb.days())


@router.callback_query(F.data.startswith('rec_cancellation_'))
async def edit_rec(callback: CallbackQuery):
    await callback.answer('')
    await bot.delete_message(chat_id='-1002186891939', message_id=int(
        c.execute(f"""SELECT mesage_id FROM {callback.data.replace('rec_cancellation_', '')} WHERE username = {str(callback.from_user.id)}""").fetchall()[0][0]))
    c.execute(f"""DELETE FROM {callback.data.replace('rec_cancellation_', '')} WHERE username = '{callback.from_user.id}'""")
    db.commit()
    c.execute(f'UPDATE user SET {callback.data.replace('rec_cancellation_', '')} = 1 WHERE user_name = {callback.from_user.id}')
    db.commit()
    await callback.message.edit_text('Запись отменена')


@router.message(F.text, fsm.Registration.people_group)
async def empty_handler(message: Message, state: FSMContext):
    await state.update_data(people_group=f'{message.text}')
    data = await state.get_data()
    if int(data['duration']) == data['duration']:
        data['duration'] = int(data['duration'])
    mes = await bot.send_message("-1002186891939",
                                 f"Новая запись на {get_date_of_weekday(data['day'])}:\n"
                                 f"Площадка - {data['place']}\n"
                                 f"Время начала - {data['time_start']}\n"
                                 f"Длительность записи - {data['duration']} часа\n"
                                 f"Информация о записанных людях:\n"
                                 f"{data['people_group']}")
    c.execute(f"""
                    INSERT INTO {data['place']} (username, day, time_start, duration, people_group, mesage_id)
                    VALUES (?, ?, ?, ?, ?, ?);
                """, (data['username'], data['day'], data['time_start'],
                      data['duration'], data['people_group'], f'{mes.message_id}'))
    db.commit()
    await message.answer('Запись успешно добавлена', reply_markup=kb.main)
    c.execute(f"""UPDATE user
                SET {data['place']} = 0 WHERE user_name = {data['username']};""")
    db.commit()


@router.message()
async def empty_handlers(message: Message):
    await message.answer('Наверное я вас не так понял, проверьте правильность сообщения')
    await message.answer_sticker('CAACAgIAAxkBAAEMoJ9mtlZLkbGXWas11BUXexN-I1WChgAC1UkAAtOjkUux-DPRTXoxATUE')
