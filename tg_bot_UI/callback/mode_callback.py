from aiogram.filters.callback_data import CallbackData

class ChangeModeCallBack(CallbackData, prefix='change'):
    mode: str


class RephraseCallBack(CallbackData, prefix='rephrase'):
    ...