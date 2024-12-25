from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove

from services.web_tools import end_connection

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if "driver" in user_data and user_data["driver"] is not None:
        end_connection(user_data["driver"])
    await state.clear()
    await message.answer(
        text="Здравствуйте! Если хотите начать просмотр учебного плана, "
        "то введите команду (/study_plan). "
        "Если на каком-то шаге захотите прекратить поиск учебного "
        "плана, то введите команду (/cancel)",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(default_state, Command(commands=["cancel"]))
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await message.answer(
        text=(
            "В данный момент вы не выбираете учебный план. "
            "Если хотите начать, то введите команду (/study_plan)"
        ),
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Command(commands=["cancel"]))
async def cmd_cancel(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if "driver" in user_data and user_data["driver"] is not None:
        end_connection(user_data["driver"])
    await state.clear()
    await message.answer(
        text=(
            "Вы закончили выбор и просмотр учебного плана. "
            "Если захотите начать заново, просто введите (/study_plan)"
        ),
        reply_markup=ReplyKeyboardRemove(),
    )
