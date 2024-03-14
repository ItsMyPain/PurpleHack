from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from clickhouse_client import ClickHouse
from embedding_client import Embedding
from fsm import Mode
from llama_client import Llama
from middleware import ChatActionMiddleware
import utils
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardMarkup
from callback import RephraseCallBack


ch = ClickHouse()
embeddings = Embedding()
llama = Llama()

router = Router()
router.message.middleware(ChatActionMiddleware())

LAST_ANSWER = ''
rephrase_kb = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text='Исправить ответ', callback_data=RephraseCallBack().pack())
    ]])


@router.message(StateFilter(Mode.silent), lambda message: not message.text.startswith('/'))
async def silent_mode(message: Message, state: FSMContext):
    question = message.text

    res = embeddings.embedding_request(question, 'len')
    questions = ch.select_question(res.get('data')).result_rows

    if len(questions) > 0:
        await message.answer(f'Найдены схожие вопросы в базе FAQ:')
        for i, q in enumerate(questions):
            question_text = f'<b>{i+1}){q[0]}</b>'
            answer_text = f'{q[1]}'
            await message.answer(text=question_text + '\n\n' + answer_text, parse_mode='HTML')

    tmp_msg = await message.answer("<i>Модель генерирует ответ в тихом режиме, пожалуйста подождите. Это не должно занять больше 2-ух минут. Если хотите посмотреть промежуточные этапы, измените режим работы бота.</i>⏱️")

    user_prompt = f"""Paraphrase the following text in three different ways. Return the result in Russian. The answer should be in the format “1) ..., 2) ...,3) ...".
    
    Text: {question}
    
    Answer:"""

    auth = llama.llama_request(user_prompt)

    ans = auth.get('data')[auth.get('data').rfind('Answer:'):]
    question_1 = ans[ans.rfind('1)'):ans.rfind('2)')]
    question_2 = ans[ans.rfind('2)'):ans.rfind('3)')]
    question_3 = ans[ans.rfind('3)'):]

    print("--------------------------")
    print(question_1)
    print(question_2)
    print(question_3)
    print("--------------------------")

    links = []
    texts = []

    res = embeddings.embedding_request(question, 'len')
    data = ch.select_document(res.get('data')).result_rows[0]
    texts.append(data[2])
    links.append(f"1) {data[0]}\nпараграф {data[1]}")

    res_1 = embeddings.embedding_request(question_1, 'len')
    data_1 = ch.select_document(res_1.get('data')).result_rows[0]
    texts.append(data_1[2])
    links.append(f"2) {data_1[0]}\nпараграф {data_1[1]}")

    res_2 = embeddings.embedding_request(question_2, 'len')
    data_2 = ch.select_document(res_2.get('data')).result_rows[0]
    texts.append(data_2[2])
    links.append(f"3) {data_2[0]}\nпараграф {data_2[1]}")

    res_3 = embeddings.embedding_request(question_3, 'len')
    data_3 = ch.select_document(res_3.get('data')).result_rows[0]
    texts.append(data_3[2])
    links.append(f"4) {data_3[0]}\nпараграф {data_3[1]}")

    for t in texts:
        print(f'\nTEXT = {t}')

    links = '\n'.join(links)
    texts = '\n'.join(texts)

    print(texts)
    print("--------------------------")
    

    user_prompt = f"""Use the following context to answer the question in Russian.
    Context:{texts}

    Question: {question}

    Answer:"""

    auth = llama.llama_request(user_prompt)
    ans = auth.get('data')
    answer = ans[ans.rfind('Answer:'):]
    answer = answer.replace('Answer:', '<b>Итоговый ответ:</b>')
    answer = utils.post_process(answer)
    global LAST_ANSWER
    LAST_ANSWER = answer
    await message.answer(text=f"""{answer}\n<b>Найдены следующие документы:</b>\n{links}""", reply_markup=rephrase_kb)

    await tmp_msg.delete()


@router.message(StateFilter(None, Mode.detailed), lambda message: not message.text.startswith('/'))
async def detailed_mode(message: Message, state: FSMContext):
    question = message.text
    question = await utils.preprocess_input_prompt(question)


    res = embeddings.embedding_request(question, 'len')
    questions = ch.select_question(res.get('data')).result_rows

    if len(questions) > 0:
        await message.answer(f'Найдены схожие вопросы в базе FAQ:')
        for i, q in enumerate(questions):
            question_text = f'<b>{i+1}){q[0]}</b>'
            answer_text = f'{q[1]}'
            await message.answer(text=question_text + '\n\n' + answer_text, parse_mode='HTML')
    else:
        await message.answer(f'Схожие вопросы не найдены в базе FAQ:')

    tmp_msg = await message.answer("<i>Модель генерирует ответ в подробном режиме, пожалуйста подождите. Это не должно занять больше 2-ух минут.</i>⏱️ \n")


    user_prompt = f"""Paraphrase the following text in three different ways. Return the result in Russian. The answer should be in the format “1) ..., 2) ...,3) ...".

    Text: {question}

    Answer:"""

    auth = llama.llama_request(user_prompt)

    ans = auth.get('data')[auth.get('data').rfind('Answer:'):]
    question_1 = ans[ans.rfind('1)'):ans.rfind('2)')]
    question_2 = ans[ans.rfind('2)'):ans.rfind('3)')]
    question_3 = ans[ans.rfind('3)'):]
    
    preprocessed_text = f'<b>Предобработанный запрос: </b>\n{question}'
    rephrased_questions = f"<b>Модель предалагает следующие переформулировки вопроса: </b>\n{question_1}{question_2}{question_3}"
    await message.answer(text=preprocessed_text + '\n\n' + rephrased_questions)

    links = []
    texts = []

    res = embeddings.embedding_request(question, 'len')
    data = ch.select_document(res.get('data')).result_rows[0]
    texts.append(data[2])
    links.append(f"1) {data[0]}\nпараграф {data[1]}")

    res_1 = embeddings.embedding_request(question_1, 'len')
    data_1 = ch.select_document(res_1.get('data')).result_rows[0]
    texts.append(data_1[2])
    links.append(f"2) {data_1[0]}\nпараграф {data_1[1]}")

    res_2 = embeddings.embedding_request(question_2, 'len')
    data_2 = ch.select_document(res_2.get('data')).result_rows[0]
    texts.append(data_2[2])
    links.append(f"3) {data_2[0]}\nпараграф {data_2[1]}")

    res_3 = embeddings.embedding_request(question_3, 'len')
    data_3 = ch.select_document(res_3.get('data')).result_rows[0]
    texts.append(data_3[2])
    links.append(f"4) {data_3[0]}\nпараграф {data_3[1]}")

    links = '\n'.join(links)
    texts = '\n'.join(texts)

    await message.answer(text=f"<b>В базе были найдены следующие документы:</b>\n{links}")

    user_prompt = f"""Use the following context to answer the question in Russian.
    Context:{texts}

    Question: {question}

    Answer:"""

    auth = llama.llama_request(user_prompt)
    ans = auth.get('data')
    answer = ans[ans.rfind('Answer:'):]
    answer = answer.replace('Answer:', '<b>Итоговый ответ:</b>')
    #await message.answer(text=answer, parse_mode='HTML')
    print(f'Answer BEFORE: {answer}')
    global LAST_ANSWER
    LAST_ANSWER = answer
    answer = utils.post_process(answer)

   

    await message.answer(text=f"""{answer}\n<b>Список документов:</b>\n{links}""", reply_markup=rephrase_kb)
    
    await tmp_msg.delete()


@router.callback_query(RephraseCallBack.filter())
async def rephrase(query: CallbackQuery, callback_data: RephraseCallBack):
    new_answer = utils.double_translate(LAST_ANSWER)
    await query.message.answer(text=new_answer)
    await query.answer()