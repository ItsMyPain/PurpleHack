import os

# import torch
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_basicauth import BasicAuth

# from transformers import AutoModelForCausalLM, AutoTokenizer
# from transformers import BitsAndBytesConfig

load_dotenv()

# tokenizer = AutoTokenizer.from_pretrained("OpenAssistant/llama2-13b-orca-8k-3319", use_fast=False)
# model = AutoModelForCausalLM.from_pretrained("OpenAssistant/llama2-13b-orca-8k-3319", torch_dtype=torch.float16,
#                                              low_cpu_mem_usage=True, device_map="cuda:0",
#                                              quantization_config=BitsAndBytesConfig(load_in_4bit=True))
System_message = "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."
Top_p = 0.95
Top_k = 0
Max_new_tokens = 256

app = Flask(__name__)
basic_auth = BasicAuth(app)
app.config['BASIC_AUTH_FORCE'] = True
app.config['BASIC_AUTH_USERNAME'] = os.getenv('FLASK_USER')
app.config['BASIC_AUTH_PASSWORD'] = os.getenv('FLASK_PASS')


@basic_auth.required
@app.route('/model', methods=['POST'])
def model():
    data = request.json
    print(data)
    user_prompt = data.get('user_prompt', False)

    if not user_prompt:
        return jsonify('Need user_prompt key'), 400

    system_message = data.get('system_message', System_message)
    top_p = data.get('top_p', Top_p)
    top_k = data.get('top_k', Top_k)
    max_new_tokens = data.get('max_new_tokens', Max_new_tokens)

    # inputs = tokenizer(f"""<|system|>{system_message}</s><|prompter|>{user_prompt}</s><|assistant|>""",
    #                    return_tensors="pt").to("cuda")
    # output = model.generate(**inputs, do_sample=True, top_p=top_p, top_k=top_k, max_new_tokens=max_new_tokens)
    # output = tokenizer.decode(output[0], skip_special_tokens=True)
    output = 'test answer from model'
    return jsonify(system_message=system_message, top_p=top_p, top_k=top_k, max_new_tokens=max_new_tokens,
                   user_prompt=user_prompt, data=output)


if __name__ == '__main__':
    app.run(host=os.getenv('FLASK_HOST'), port=os.getenv('FLASK_PORT'))
