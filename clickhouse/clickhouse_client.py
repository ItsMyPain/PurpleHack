import os

import clickhouse_connect
from dotenv import load_dotenv

load_dotenv()


class ClickHouse:
    def __init__(self):
        self.client = clickhouse_connect.get_client(host=os.getenv('CH_HOST'), port=int(os.getenv('CH_PORT')),
                                                    username=os.getenv('CH_USER'), password=os.getenv('CH_PASS'))

    def create_table(self):
        self.client.command("""
        CREATE TABLE document( 
            url String,
            embedding Array(Float32),
            paragraph Nullable(String),
            text String
        )
        ENGINE = MergeTree()
        ORDER BY embedding;
        """)

    def insert(self, data: list[list]):
        self.client.insert('document', data, column_names=['url', 'embedding', 'paragraph', 'text'])

    def select(self, data: list[float]):
        return self.client.query("""
        SELECT url, paragraph, text, cosineDistance({data:Array(Float32)}, embedding) AS score 
        FROM document 
        ORDER BY score DESC 
        LIMIT 10
        """, parameters={'data': data})


if __name__ == '__main__':
    ch = ClickHouse()
    import json

    ch.create_table()
    f = open('data_txt.json')
    data = json.load(f)
    input_data = []
    for i in data:
      input_data.append([i['url'], i['embedding'], i['paragraph'], i['text']])
    ch.insert(input_data)
