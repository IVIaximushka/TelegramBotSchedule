from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Здравствуйте! Если хотите начать просмотр "
             "учебного плана, то введите команду (/study_plan)",
        reply_markup=ReplyKeyboardRemove(),
    )
