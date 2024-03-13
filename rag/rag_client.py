from dotenv import load_dotenv

from clickhouse_client import ClickHouse
from embedding_client import Embedding
from llama_client import Llama

load_dotenv()

if __name__ == '__main__':
    ch = ClickHouse()
    embeddings = Embedding()
    llama = Llama()

    # Question = """Кем назначается Уполномоченный представитель Банка России?"""
    Question = """Как зовут председателя центрального банка российской федерации?"""
    # Question = """Скачать обо клеш рояль"""

    res = embeddings.embedding_request(Question, 'len')
    questions = ch.select_question(res.get('data')).result_rows

    user_prompt = f"""Paraphrase the following text in three different ways. Return the result in Russian. The answer should be in the format “1) ..., 2) ...,3) ...".
    
    Text: {Question}
    
    Answer:"""

    auth = llama.llama_request(user_prompt)

    ans = auth.get('data')[auth.get('data').rfind('Answer:'):]
    Question_1 = ans[ans.rfind('1)'):ans.rfind('2)')]
    Question_2 = ans[ans.rfind('2)'):ans.rfind('3)')]
    Question_3 = ans[ans.rfind('3)'):]
    print("--------------------------")
    print(Question_1)
    print(Question_2)
    print(Question_3)
    print("--------------------------")
    links = []
    text_to_ans = []

    res = embeddings.embedding_request(Question, 'len')
    data = ch.select_document(res.get('data')).result_rows[0]
    text_to_ans.append(data[2])
    links.append(data[0])

    res_1 = embeddings.embedding_request(Question_1, 'len')
    data_1 = ch.select_document(res_1.get('data')).result_rows[0]
    text_to_ans.append(data_1[2])
    links.append(data_1[0])

    res_2 = embeddings.embedding_request(Question_2, 'len')
    data_2 = ch.select_document(res_2.get('data')).result_rows[0]
    text_to_ans.append(data_2[2])
    links.append(data_2[0])

    res_3 = embeddings.embedding_request(Question_3, 'len')
    data_3 = ch.select_document(res_3.get('data')).result_rows[0]
    text_to_ans.append(data[2])
    links.append(data[0])

    links = '\n'.join(links)
    text_to_ans = '\n'.join(text_to_ans)

    print(text_to_ans)
    print("--------------------------")

    user_prompt = f"""Use the following context to answer the question in Russian.

    Context:{text_to_ans}

    Question: {Question}
    
    Answer:"""

    auth = llama.llama_request(user_prompt)
    ans = auth.get('data')
    print(ans[ans.rfind('Answer:'):])
