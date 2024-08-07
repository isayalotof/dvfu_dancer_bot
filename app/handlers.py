from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from app import keyboard as kb, fsm
from aiogram.fsm.context import FSMContext
from data.data_base import c


count_rec = True

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Здравствуйте, {message.from_user.first_name}',
                        reply_markup=kb.main)
    info_user = c.execute(f'SELECT user_name FROM user WHERE user_name = {message.from_user.id}').fetchall()
    if len(info_user) > 0:
        pass
    else:
        c.execute(f"""INSERT INTO user
        (user_name, count_rec)
        VALUES
        ('{message.from_user.id}', 1)
        """)


@router.message(F.text == 'Новая запись')
async def new_record(message: Message, state: FSMContext):
    if count_rec:
        await state.set_state(fsm.Reg.place())
        await message.answer(f'Выберите площадку:', reply_markup=kb.place)


@router.callback_query(F.data == 'Place1')
async def set_place(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(place='Place1')
    await callback.message.edit_text('Выберите время начала:')


