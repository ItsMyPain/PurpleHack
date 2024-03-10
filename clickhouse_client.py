import os

from dotenv import load_dotenv
from infi.clickhouse_orm import Model, StringField, Float32Field, MergeTree, ArrayField, Database, UInt16Field

load_dotenv()


class Document(Model):
    __tablename__ = 'document'

    id = UInt16Field()
    title = StringField()
    embedding = ArrayField(Float32Field())

    engine = MergeTree(partition_key=['id'], order_by=['id'])


db = Database(os.getenv('CH_DATABASE'), db_url=os.getenv('CH_URL'), username=os.getenv('CH_USER'),
              password=os.getenv('CH_PASS'))
db.drop_table(Document)
db.create_table(Document)
