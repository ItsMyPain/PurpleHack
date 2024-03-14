# PurpleHack

## Описание
Проект представляет собой *Retrieval Augmented Generation* в основе которой лежит *Llama 2*


Папки *clickhouse*, *embedding* и *llama* содержат в себе докер контейнеры серверов.
1. *clickhouse* - разварачивает *СlickHouse*
2. *embedding/server.py* генерируют эмэдинги с помощью модели *e5-base-v2*
3. *embedding/server.py* Поднимает модель *llama2-13b-orca-8k-3319*


Папка *rag* содержит в себе все этапы запроса от клиента:
1. *rag/clickhouse_client.py* - класс взаимодействия *СlickHouse* (поиск по по косинусноуму расстоянию по таблицам документов и вопросов)
2. *rag/embedding_client.py* - класс для создания *embeddings*
3. *rag/llama_client.py* - класс для взаимодействия с  *Llama2*
4. *rag/rag_client.py* - поэтапно прописанная реализация  *retrieval augmented generation*


Папка *tg_bot_UI* содержит в себе реализацию telegramm бота для удобного взаимодействия с системой
