from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from app import keyboard as kb, fsm
from aiogram.fsm.context import FSMContext
from main import bot
from data.datatime import get_date_of_weekday
from data.data_base import c, db

db_path = "data.db"
s = {}
rec_plas = ''
router = Router()
user_named = 0


@router.message(CommandStart())
async def cmd_start(message: Message):
    global user_named
    user_named = message.from_user.id
    await message.answer(f'Здравствуйте, {message.from_user.first_name.capitalize()}',
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


@router.message(F.text == 'Мои записи')
async def new_record(message: Message):
    global user_named
    user_named = message.from_user.id
    await message.answer('Ваши записи:', reply_markup=await kb.get_rec())


@router.message(F.text == 'Информация')
async def my_info(message: Message):
    await message.answer("Информация, когда мне датут тг админа я прифигачу сюда его контакты, а пока хз")


@router.callback_query(F.data == 'Place1')
async def set_place(callback: CallbackQuery, state: FSMContext):
    if 0 in c.execute(f"""SELECT Place1 FROM user WHERE user_name = {callback.from_user.id};""").fetchone():
        await callback.answer('')
        await callback.message.edit_text('У вас не осталось записей на эту площадку\n'
                                         'попробуйте выбрать другую или приходите в понедельник:',
                                         reply_markup=kb.place)
    else:
        await callback.answer('')
        await state.update_data(place='Place1')
        global s
        s['Place'] = 'Place1'
        await state.set_state(fsm.Reg.day)
        await callback.message.edit_text(f'Выберите день для записи: ', reply_markup=await kb.days())


@router.callback_query(F.data == 'Place2')
async def set_place(callback: CallbackQuery, state: FSMContext):
    if 0 in c.execute(f"""SELECT Place2 FROM user WHERE user_name = {callback.from_user.id};"""):
        await callback.answer('')
        await callback.message.edit_text('У вас не осталось записей на эту площадку\n'
                                         'попробуйте выбрать другую или приходите в понедельник:',
                                         reply_markup=kb.place)
    else:
        await callback.answer('')
        await state.update_data(place='Place2')
        global s
        s['Place'] = 'Place2'
        await state.set_state(fsm.Reg.day)
        await callback.message.edit_text(f'Выберите день для записи: ', reply_markup=await kb.days())


@router.callback_query(F.data == 'Place3')
async def set_place(callback: CallbackQuery, state: FSMContext):
    if 0 in c.execute(f"""SELECT Place3 FROM user WHERE user_name = {callback.from_user.id};"""):
        await callback.answer('')
        await callback.message.edit_text('У вас не осталось записей на эту площадку\n'
                                         'попробуйте выбрать другую или приходите в понедельник:',
                                         reply_markup=kb.place)
    else:
        await callback.answer('')
        await state.update_data(place='Place3')
        global s
        s['Place'] = 'Place3'
        await state.set_state(fsm.Reg.day)
        await callback.message.edit_text(f'Выберите день для записи: ', reply_markup=await kb.days())


@router.callback_query(F.data == 'Place4')
async def set_place(callback: CallbackQuery, state: FSMContext):
    if 0 in c.execute(f"""SELECT Place4 FROM user WHERE user_name = {callback.from_user.id};"""):
        await callback.answer('')
        await callback.message.edit_text('У вас не осталось записей на эту площадку\n'
                                         ' попробуйте выбрать другую или приходите в понедельник:',
                                         reply_markup=kb.place)
    else:
        await callback.answer('')
        await state.update_data(place='Place4')
        global s
        s['Place'] = 'Place4'
        await state.set_state(fsm.Reg.day)
        await callback.message.edit_text(f'Выберите день для записи: ', reply_markup=await kb.days())


@router.callback_query(F.data == 'понедельник')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(day='Monday')
    global s
    s['day'] = 'Monday'
    await state.set_state(fsm.Reg.time_start)
    await callback.message.edit_text('Выберите время начала', reply_markup=await kb.available_slot())


@router.callback_query(F.data == 'Вторник')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(day='Tuesday')
    global s
    s['day'] = 'Tuesday'
    await state.set_state(fsm.Reg.time_start)
    await callback.message.edit_text('Выберите время начала', reply_markup=await kb.available_slot())


@router.callback_query(F.data == 'Среда')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(day='Wednesday')
    global s
    s['day'] = 'Wednesday'
    await state.set_state(fsm.Reg.time_start)
    await callback.message.edit_text('Выберите время начала', reply_markup=await kb.available_slot())


@router.callback_query(F.data == 'Четверг')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(day='Thursday')
    global s
    s['day'] = 'Thursday'
    await state.set_state(fsm.Reg.time_start)
    await callback.message.edit_text('Выберите время начала', reply_markup=await kb.available_slot())


@router.callback_query(F.data == 'Пятница')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(day='Friday')
    global s
    s['day'] = 'Friday'
    await state.set_state(fsm.Reg.time_start)
    await callback.message.edit_text('Выберите время начала', reply_markup=await kb.available_slot())


@router.callback_query(F.data == 'Суббота')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(day='Saturday')
    global s
    s['day'] = 'Saturday'
    await state.set_state(fsm.Reg.time_start)
    await callback.message.edit_text('Выберите время начала', reply_markup=await kb.available_slot())


@router.callback_query(F.data == 'Воскресенье')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(day='Sunday')
    global s
    s['day'] = 'Sunday'
    await state.set_state(fsm.Reg.time_start)
    await callback.message.edit_text('Выберите время начала', reply_markup=await kb.available_slot())


@router.callback_query(F.data == '10:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='10:00')
    global s
    s['time_start'] = '10:00'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберите длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '10:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='10:30')
    global s
    s['time_start'] = '10:30'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберите длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '11:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='11:00')
    global s
    s['time_start'] = '11:00'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберите длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '11:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='11:30')
    global s
    s['time_start'] = '11:30'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберите длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '12:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='12:00')
    global s
    s['time_start'] = '12:00'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберите длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '12:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='12:30')
    global s
    s['time_start'] = '12:30'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберите длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '13:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='13:00')
    global s
    s['time_start'] = '13:00'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберите длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '13:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='13:30')
    global s
    s['time_start'] = '13:30'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберите длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '14:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='14:00')
    global s
    s['time_start'] = '14:00'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберите длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '14:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='14:30')
    global s
    s['time_start'] = '14:30'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберите длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '15:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='15:00')
    global s
    s['time_start'] = '15:00'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберите длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '15:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='15:30')
    global s
    s['time_start'] = '15:30'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберите длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '16:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='16:00')
    global s
    s['time_start'] = '16:00'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберите длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '16:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='16:30')
    global s
    s['time_start'] = '16:30'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберите длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '17:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='17:00')
    global s
    s['time_start'] = '17:00'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберите длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '17:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='17:30')
    global s
    s['time_start'] = '17:30'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберите длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '18:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='18:00')
    global s
    s['time_start'] = '18:00'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберите длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '18:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='18:30')
    global s
    s['time_start'] = '18:30'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберите длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '19:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='19:00')
    global s
    s['time_start'] = '19:00'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберите длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '19:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='19:30')
    global s
    s['time_start'] = '19:30'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберите длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '20:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='20:00')
    global s
    s['time_start'] = '20:00'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберите длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '20:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='20:30')
    global s
    s['time_start'] = '20:30'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберите длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '21:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='21:00')
    global s
    s['time_start'] = '21:00'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберите длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '21:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(time_start='21:30')
    global s
    s['time_start'] = '21:30'
    await state.set_state(fsm.Reg.duration)
    await callback.message.edit_text("Выберите длительность: ", reply_markup=await kb.durations())


@router.callback_query(F.data == '0:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(duration=0.5)
    await state.set_state(fsm.Reg.people_group)
    await callback.message.edit_text(f"Отправьте ФИО всех кто придет по этой записи\n"
                                     f"Обратите внимание,\n"
                                     f"Все люди должны быть указанны и пронумерованны\n"
                                     f"Пример:\n"
                                     f"1) Гуманоид 1\n"
                                     f"2) Гуманоид 2\n"
                                     f"и тд \n")


@router.callback_query(F.data == '1:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(duration=1.0)
    await state.set_state(fsm.Reg.people_group)
    await callback.message.edit_text(f"Отправьте ФИО всех кто придет по этой записи\n"
                                     f"Обратите внимание,\n"
                                     f"Все люди должны быть указанны и пронумерованны\n"
                                     f"Пример:\n"
                                     f"1) Гуманоид 1\n"
                                     f"2) Гуманоид 2\n"
                                     f"и тд \n")


@router.callback_query(F.data == '1:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(duration=1.5)
    await state.set_state(fsm.Reg.people_group)
    await callback.message.edit_text(f"Отправьте ФИО всех кто придет по этой записи\n"
                                     f"Обратите внимание,\n"
                                     f"Все люди должны быть указанны и пронумерованны\n"
                                     f"Пример:\n"
                                     f"1) Гуманоид 1\n"
                                     f"2) Гуманоид 2\n"
                                     f"и тд \n")


@router.callback_query(F.data == '2:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(duration=2.0)
    await state.set_state(fsm.Reg.people_group)
    await callback.message.edit_text(f"Отправьте ФИО всех кто придет по этой записи\n"
                                     f"Обратите внимание,\n"
                                     f"Все люди должны быть указанны и пронумерованны\n"
                                     f"Пример:\n"
                                     f"1) Гуманоид 1\n"
                                     f"2) Гуманоид 2\n"
                                     f"и тд \n")


@router.callback_query(F.data == '2:30')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(duration=2.5)
    await state.set_state(fsm.Reg.people_group)
    await callback.message.edit_text(f"Отправьте ФИО всех кто придет по этой записи\n"
                                     f"Обратите внимание,\n"
                                     f"Все люди должны быть указанны и пронумерованны\n"
                                     f"Пример:\n"
                                     f"1) Гуманоид 1\n"
                                     f"2) Гуманоид 2\n"
                                     f"и тд \n")


@router.callback_query(F.data == '3:00')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(duration=3.0)
    await state.set_state(fsm.Reg.people_group)
    await callback.message.edit_text(f"Отправьте ФИО всех кто придет по этой записи\n"
                                     f"Обратите внимание,\n"
                                     f"Все люди должны быть указанны и пронумерованны\n"
                                     f"Пример:\n"
                                     f"1) Гуманоид 1\n"
                                     f"2) Гуманоид 2\n"
                                     f"и тд \n")


@router.callback_query(F.data == 'rec_Place1')
async def my_rec_place(callback: CallbackQuery):
    await callback.answer('')
    global rec_plas
    rec_plas = 'Place1'
    await callback.message.edit_text(f"Запись на Place1, что хотите сделать?", reply_markup=await kb.my_menu())


@router.callback_query(F.data == 'rec_Place2')
async def my_rec_place(callback: CallbackQuery):
    await callback.answer('')
    global rec_plas
    rec_plas = 'Place2'
    await callback.message.edit_text(f"Запись на Place2, что хотите сделать?", reply_markup=await kb.my_menu())


@router.callback_query(F.data == 'rec_Place3')
async def my_rec_place(callback: CallbackQuery):
    await callback.answer('')
    global rec_plas
    rec_plas = 'Place3'
    await callback.message.edit_text(f"Запись на Place3, что хотите сделать?", reply_markup=await kb.my_menu())


@router.callback_query(F.data == 'rec_Place4')
async def my_rec_place(callback: CallbackQuery):
    await callback.answer('')
    global rec_plas
    rec_plas = 'Place4'
    await callback.message.edit_text(f"Запись на Place4, что хотите сделать?", reply_markup=await kb.my_menu())


@router.callback_query(F.data == 'rec_edit_Place1')
async def edit_rec(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    mes_id = c.execute(f"""SELECT mesage_id FROM Place1 WHERE username = {str(callback.from_user.id)}""").fetchall()
    await bot.delete_message(chat_id='-1002186891939', message_id=int(mes_id[0][0]))
    c.execute(f"""DELETE FROM Place1 WHERE username = {callback.from_user.id}""")
    db.commit()
    global user_named
    user_named = callback.from_user.id
    await state.set_state(fsm.Reg.username)
    await state.update_data(username=f"{callback.from_user.id}")
    await state.set_state(fsm.Reg.place)
    await callback.answer('')
    await state.update_data(place='Place1')
    s['Place'] = 'Place1'
    await state.set_state(fsm.Reg.day)
    await callback.message.edit_text(f'Выберите день для записи: ', reply_markup=await kb.days())


@router.callback_query(F.data == 'rec_edit_Place2')
async def edit_rec(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    mes_id = c.execute(f"""SELECT mesage_id FROM Place2 WHERE username = {str(callback.from_user.id)}""").fetchall()
    await bot.delete_message(chat_id='-1002186891939', message_id=int(mes_id[0][0]))
    c.execute(f"""DELETE FROM Place2 WHERE username = {callback.from_user.id}""")
    db.commit()
    global user_named
    user_named = callback.from_user.id
    await state.set_state(fsm.Reg.username)
    await state.update_data(username=f"{callback.from_user.id}")
    await state.set_state(fsm.Reg.place)
    await callback.answer('')
    await state.update_data(place='Place2')
    s['Place'] = 'Place2'
    await state.set_state(fsm.Reg.day)
    await callback.message.edit_text(f'Выберите день для записи: ', reply_markup=await kb.days())


@router.callback_query(F.data == 'rec_edit_Place3')
async def edit_rec(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    mes_id = c.execute(f"""SELECT mesage_id FROM Place3 WHERE username = {str(callback.from_user.id)}""").fetchall()
    await bot.delete_message(chat_id='-1002186891939', message_id=int(mes_id[0][0]))
    c.execute(f"""DELETE FROM Place3 WHERE username = {callback.from_user.id}""")
    db.commit()
    global user_named
    user_named = callback.from_user.id
    await state.set_state(fsm.Reg.username)
    await state.update_data(username=f"{callback.from_user.id}")
    await state.set_state(fsm.Reg.place)
    await callback.answer('')
    await state.update_data(place='Place3')
    s['Place'] = 'Place3'
    await state.set_state(fsm.Reg.day)
    await callback.message.edit_text(f'Выберите день для записи: ', reply_markup=await kb.days())


@router.callback_query(F.data == 'rec_edit_Place4')
async def edit_rec(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    mes_id = c.execute(f"""SELECT mesage_id FROM Place4 WHERE username = {str(callback.from_user.id)}""").fetchall()
    await bot.delete_message(chat_id='-1002186891939', message_id=int(mes_id[0][0]))
    c.execute(f"""DELETE FROM Place4 WHERE username = {callback.from_user.id}""")
    db.commit()
    global user_named
    user_named = callback.from_user.id
    await state.set_state(fsm.Reg.username)
    await state.update_data(username=f"{callback.from_user.id}")
    await state.set_state(fsm.Reg.place)
    await callback.answer('')
    await state.update_data(place='Place4')
    s['Place'] = 'Place4'
    await state.set_state(fsm.Reg.day)
    await callback.message.edit_text(f'Выберите день для записи: ', reply_markup=await kb.days())


@router.callback_query(F.data == 'rec_cancellation_Place1')
async def edit_rec(callback: CallbackQuery):
    await callback.answer('')
    mes_id = c.execute(f"""SELECT mesage_id FROM Place1 WHERE username = {str(callback.from_user.id)}""").fetchall()
    await bot.delete_message(chat_id='-1002186891939', message_id=int(mes_id[0][0]))
    c.execute(f"""DELETE FROM Place1 WHERE username = '{callback.from_user.id}'""")
    db.commit()
    c.execute(f'UPDATE user SET Place1 = 1 WHERE user_name = {callback.from_user.id}')
    db.commit()
    await callback.message.edit_text('Запись отменена')


@router.callback_query(F.data == 'rec_cancellation_Place2')
async def edit_rec(callback: CallbackQuery):
    await callback.answer('')
    mes_id = c.execute(f"""SELECT mesage_id FROM Place2 WHERE username = {str(callback.from_user.id)}""").fetchall()
    await bot.delete_message(chat_id='-1002186891939', message_id=int(mes_id[0][0]))
    c.execute(f"""DELETE FROM Place2 WHERE username = '{callback.from_user.id}'""")
    db.commit()
    c.execute(f'UPDATE user SET Place2 = 1 WHERE user_name = {callback.from_user.id}')
    db.commit()
    await callback.message.edit_text('Запись отменена')


@router.callback_query(F.data == 'rec_cancellation_Place3')
async def edit_rec(callback: CallbackQuery):
    await callback.answer('')
    mes_id = c.execute(f"""SELECT mesage_id FROM Place3 WHERE username = {str(callback.from_user.id)}""").fetchall()
    await bot.delete_message(chat_id='-1002186891939', message_id=int(mes_id[0][0]))
    c.execute(f"""DELETE FROM Place3 WHERE username = '{callback.from_user.id}'""")
    db.commit()
    c.execute(f'UPDATE user SET Place3 = 1 WHERE user_name = {callback.from_user.id}')
    db.commit()
    await callback.message.edit_text('Запись отменена')


@router.callback_query(F.data == 'rec_cancellation_Place4')
async def edit_rec(callback: CallbackQuery):
    await callback.answer('')
    mes_id = c.execute(f"""SELECT mesage_id FROM Place4 WHERE username = {str(callback.from_user.id)}""").fetchall()
    await bot.delete_message(chat_id='-1002186891939', message_id=int(mes_id[0][0]))
    c.execute(f"""DELETE FROM Place4 WHERE username = '{callback.from_user.id}'""")
    db.commit()
    c.execute(f'UPDATE user SET Place4 = 1 WHERE user_name = {callback.from_user.id}')
    db.commit()
    await callback.message.edit_text('Запись отменена')


@router.message()
async def empty_handler(message: Message, state: FSMContext):
    if '1' in message.text and ')' in message.text:
        await state.update_data(people_group=f'{message.text}')
        data = await state.get_data()
        table_name = data['place']
        mes = await bot.send_message("-1002186891939",
                                     f"Новая запись на {get_date_of_weekday(data['day'])}:\n"
                                     f"Время начала - {data['time_start']}\n"
                                     f"Длительность записи - {data['duration']}\n"
                                     f"Информация о записанных людях:\n"
                                     f"{data['people_group']}")
        c.execute(f"""
                    INSERT INTO {table_name} (username, day, time_start, duration, people_group, mesage_id)
                    VALUES (?, ?, ?, ?, ?, ?);
                """, (data['username'], data['day'], data['time_start'],
                      data['duration'], data['people_group'], f'{mes.message_id}'))
        db.commit()
        await message.answer('Запись успешно добавлена', reply_markup=kb.main)
        c.execute(f"""UPDATE user
                SET {table_name} = 0 WHERE user_name = {user_named};""")
        db.commit()
    else:
        await message.answer('Наверное я вас не так понял, проверьте правильность сообщения')
        await message.answer_sticker('CAACAgIAAxkBAAEMoJ9mtlZLkbGXWas11BUXexN-I1WChgAC1UkAAtOjkUux-DPRTXoxATUE')
