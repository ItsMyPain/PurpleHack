import os

import torch.nn.functional as F
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from torch import Tensor
from transformers import AutoTokenizer, AutoModel

load_dotenv()


def average_pool(last_hidden_states: Tensor,
                 attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


print('Loading model...')
tokenizer = AutoTokenizer.from_pretrained('intfloat/e5-base-v2')
model = AutoModel.from_pretrained('intfloat/e5-base-v2')
print('Loaded model')

app = Flask(__name__)
basic_auth = BasicAuth(app)
app.config['BASIC_AUTH_FORCE'] = True
app.config['BASIC_AUTH_USERNAME'] = os.getenv('EMBEDDING_USER')
app.config['BASIC_AUTH_PASSWORD'] = os.getenv('EMBEDDING_PASS')


@basic_auth.required
@app.route('/embedding', methods=['POST'])
def embedding():
    data = request.json
    print(data)
    input_text = data.get('input_text', False)

    if not input_text:
        return jsonify('Need input_text key'), 400

    max_length = data.get('max_length', 512)
    if max_length == 'len':
        max_length = len(input_text)
    else:
        max_length = int(max_length)

    batch_dict = tokenizer(input_text, max_length=max_length, padding=True, truncation=True, return_tensors='pt')
    outputs = model(**batch_dict)
    embeddings = average_pool(outputs.last_hidden_state, batch_dict['attention_mask'])
    embeddings = F.normalize(embeddings, p=2, dim=1)
    output = embeddings[0].detach().numpy().tolist()
    return jsonify(data=output)


if __name__ == '__main__':
    import torch

    print(torch.cuda.is_available())
    app.run(host=os.getenv('EMBEDDING_HOST'), port=os.getenv('EMBEDDING_PORT'))
