from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def message_with_text(message: Message):
    await message.answer("Это неизвестное мне сообщение!")
