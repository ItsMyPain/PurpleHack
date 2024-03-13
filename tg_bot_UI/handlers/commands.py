from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ContentType, InputFile, FSInputFile
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from fsm import Mode
from config import START_MSG, MODE_MSG, INFO_MSG, FEEDBACK_MSG
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardMarkup
from callback import ChangeModeCallBack

router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(text=START_MSG)


@router.message(Command('info'))
async def cmd_info(message: Message):
    await message.answer(text=INFO_MSG)

@router.message(Command('feedback'))
async def cmd_feedback(message: Message):
    await message.answer(text=FEEDBACK_MSG)


@router.message(StateFilter('*'), Command('mode'))
async def cmd_mode(message: Message, state: FSMContext):
    change_mode_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Подробный', callback_data=ChangeModeCallBack(mode='detailed').pack()),
                InlineKeyboardButton(text='Тихий', callback_data=ChangeModeCallBack(mode='silent').pack()),
            ]
        ])
    await message.answer(text=MODE_MSG, reply_markup=change_mode_kb)



@router.callback_query(StateFilter('*'), ChangeModeCallBack.filter())
async def change_mode(query: CallbackQuery, state: FSMContext, callback_data: ChangeModeCallBack):
    await query.message.answer(text=f'Режим изменен на {callback_data.mode}!')
    await query.message.delete()
    if callback_data.mode == 'silent':
        await state.set_state(Mode.silent)
    elif callback_data.mode == 'detailed':
        await state.set_state(Mode.detailed)
    await query.answer(text=f'Режим изменен на {callback_data.mode}!')