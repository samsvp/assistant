import argparse
from gpt4all import GPT4All
from deep_translator import GoogleTranslator

import search
from prompts import *
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit


app = Flask(__name__)
socketio = SocketIO(app)
pt_en_translator = GoogleTranslator(source='pt', target='en')
en_pt_translator = GoogleTranslator(source='en', target='pt')

def print_args(args: argparse.Namespace) -> None:
    print(f"Model path: {args.model}")
    print(f"Temperature: {args.temp}")
    print(f"Max tokens: {args.max_tokens}")
    print(f"Prompt template: {args.prompt_template}")
    print("")


@app.route('/')
def home():
    return render_template('index.html')


@socketio.on('message')
def handle_message(data):
    data = pt_en_translator.translate(data)
    results = collection.query(query_texts=[data], n_results=2)
    
    dist_1, dist_2 = results['distances'][0]
    if abs(dist_1 - dist_2) / dist_1 < 0.15: 
        prompt = prompt_function(data, results['documents'][0])
    else:
        prompt = prompt_function(data, [results['documents'][0][0]])
    print(prompt)
    
    out_str = ""
    emit("server_message", "[START]")
    for o in model.generate(prompt, temp=args.temp, 
                            max_tokens=args.max_tokens, 
                            n_batch=32,
                            streaming=True):
        out_str += o
        if o in [".", "!", "?"] and out_str[-2] not in "1234567890":
            out_str = en_pt_translator.translate(out_str)
            emit("server_message", out_str)
            print(out_str)
            out_str = ""

    emit("server_message", "[FINISHED]")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', help="Path to the model to use")
    parser.add_argument('-t', '--temp', 
                        type=int, default=0,
                        help="Model temperature")
    parser.add_argument('--prompt-template', 
                        default="alpaca",
                        help="Model temperature")
    parser.add_argument('--max-tokens', 
                        type=int, default=200,
                        help="Model temperature")
    parser.add_argument('--port', 
                        type=int, default=5050,
                        help="Flask port")
    parser.add_argument('--debug', 
                        action="store_true",
                        help="Run flask in debug mode")
    parser.add_argument('-d', '--device', 
                        default="cpu",
                        help="Run flask in debug mode")

    args = parser.parse_args()
    
    print_args(args)
    
    prompt_template = args.prompt_template
    print("Creating database")
    collection = search.create_collection("database")

    if prompt_template == 'alpaca':
        prompt_function = create_prompt_alpaca
    elif prompt_template == 'custom':
        prompt_function = create_prompt_custom
    elif prompt_template == 'gpt4':
        prompt_function = create_prompt_gpt4
    else:
        print(f'Invalid prompt template {prompt_template}')
        exit(1)

    print(f"Loading model {args.model}...")
    model = GPT4All(args.model, ".", device=args.device)
    print("Model loaded!")

    socketio.run(app, debug=args.debug, port=args.port)


