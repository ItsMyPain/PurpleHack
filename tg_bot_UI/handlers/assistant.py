from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ContentType, InputFile, FSInputFile
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from fsm import Mode
from config import START_MSG
#from utils import get_full_response, get_answer_from_bd, get_paragraps_from_documents, get_final_result
import utils
from middleware import ChatActionMiddleware
from asyncio import sleep


router = Router()
router.message.middleware(ChatActionMiddleware())

@router.message(StateFilter(None, Mode.silent), lambda message: not message.text.startswith('/'))
async def silent_mode(message: Message, state: FSMContext):
    await sleep(1)
    prompt = message.text
    response_text, response_urls = await utils.get_full_response(prompt)
    await message.answer(text=response_text + '\n' + response_urls)
    


@router.message(StateFilter(Mode.detailed), lambda message: not message.text.startswith('/'))
async def detailed_mode(message: Message, state: FSMContext):
    prompt = message.text

    answer_from_bd = await utils.get_answer_from_bd(prompt)
    await message.answer(answer_from_bd)
    await sleep(0.2)

    answer_from_documetns = await utils.get_paragraps_from_documents(prompt)
    await message.answer(answer_from_documetns)
    await sleep(0.2)

    final_answer = await utils.get_final_result(prompt)
    await message.answer(final_answer)