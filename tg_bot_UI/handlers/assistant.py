from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from clickhouse_client import ClickHouse
from embedding_client import Embedding
from fsm import Mode
from llama_client import Llama
from middleware import ChatActionMiddleware

ch = ClickHouse()
embeddings = Embedding()
llama = Llama()

router = Router()
router.message.middleware(ChatActionMiddleware())


@router.message(StateFilter(None, Mode.silent), lambda message: not message.text.startswith('/'))
async def silent_mode(message: Message, state: FSMContext):
    question = message.text
    res = embeddings.embedding_request(question, 'len')
    questions = ch.select_question(res.get('data')).result_rows

    if len(questions) > 0:
        await message.answer(f"Возможно, ваш вопрос есть среди этих:")
        for i in questions:
            await message.answer(f"{i[0]}\n\n{i[1]}")

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
    links.append(f"Документ находится по ссылке: {data[0]} в параграфе {data[1]}")

    res_1 = embeddings.embedding_request(question_1, 'len')
    data_1 = ch.select_document(res_1.get('data')).result_rows[0]
    texts.append(data_1[2])
    links.append(f"Документ находится по ссылке: {data_1[0]} в параграфе {data_1[1]}")

    res_2 = embeddings.embedding_request(question_2, 'len')
    data_2 = ch.select_document(res_2.get('data')).result_rows[0]
    texts.append(data_2[2])
    links.append(f"Документ находится по ссылке: {data_2[0]} в параграфе {data_2[1]}")

    res_3 = embeddings.embedding_request(question_3, 'len')
    data_3 = ch.select_document(res_3.get('data')).result_rows[0]
    texts.append(data_3[2])
    links.append(f"Документ находится по ссылке: {data_3[0]} в параграфе {data_3[1]}")

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
    await message.answer(text=f"""{answer}\nНайдены следующие документы:\n{links}""")


@router.message(StateFilter(Mode.detailed), lambda message: not message.text.startswith('/'))
async def detailed_mode(message: Message, state: FSMContext):
    question = message.text
    res = embeddings.embedding_request(question, 'len')
    questions = ch.select_question(res.get('data')).result_rows

    if len(questions) > 0:
        await message.answer(f"Возможно, ваш вопрос есть среди этих:")
        for i in questions:
            await message.answer(f"{i[0]}\n\n{i[1]}")

    user_prompt = f"""Paraphrase the following text in three different ways. Return the result in Russian. The answer should be in the format “1) ..., 2) ...,3) ...".

    Text: {question}

    Answer:"""

    auth = llama.llama_request(user_prompt)

    ans = auth.get('data')[auth.get('data').rfind('Answer:'):]
    question_1 = ans[ans.rfind('1)'):ans.rfind('2)')]
    question_2 = ans[ans.rfind('2)'):ans.rfind('3)')]
    question_3 = ans[ans.rfind('3)'):]

    await message.answer(text=f"Модель предалагает следующие переформулированные запросы:\n{question_1}\n{question_2}\n{question_3}")

    links = []
    texts = []

    res = embeddings.embedding_request(question, 'len')
    data = ch.select_document(res.get('data')).result_rows[0]
    texts.append(data[2])
    links.append(f"Документ находится по ссылке: {data[0]} в параграфе {data[1]}")

    res_1 = embeddings.embedding_request(question_1, 'len')
    data_1 = ch.select_document(res_1.get('data')).result_rows[0]
    texts.append(data_1[2])
    links.append(f"Документ находится по ссылке: {data_1[0]} в параграфе {data_1[1]}")

    res_2 = embeddings.embedding_request(question_2, 'len')
    data_2 = ch.select_document(res_2.get('data')).result_rows[0]
    texts.append(data_2[2])
    links.append(f"Документ находится по ссылке: {data_2[0]} в параграфе {data_2[1]}")

    res_3 = embeddings.embedding_request(question_3, 'len')
    data_3 = ch.select_document(res_3.get('data')).result_rows[0]
    texts.append(data_3[2])
    links.append(f"Документ находится по ссылке: {data_3[0]} в параграфе {data_3[1]}")

    links = '\n'.join(links)
    texts = '\n'.join(texts)

    await message.answer(text=f"В базе были найдены следующие документы:\n{links}")

    user_prompt = f"""Use the following context to answer the question in Russian.
    Context:{texts}

    Question: {question}

    Answer:"""

    auth = llama.llama_request(user_prompt)
    ans = auth.get('data')
    answer = ans[ans.rfind('Answer:'):]
    await message.answer(text=f"""{answer}\nНайдены следующие документы:\n{links}""")
