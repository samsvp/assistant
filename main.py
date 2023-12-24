import argparse
from gpt4all import GPT4All

import search
from prompts import *


def print_args(args: argparse.Namespace) -> None:
    print(f"Model path: {args.model}")
    print(f"Temperature: {args.temp}")
    print(f"Max tokens: {args.max_tokens}")
    print(f"Prompt template: {args.prompt_template}")
    print("")


def main(model_name: str, temp: float, prompt_template: str, max_tokens: int) -> None:
    collection = search.create_collection("database")
    with open("test-questions/questions.txt") as fp:
        questions = fp.read().split('\n')[:-1]

    if prompt_template == 'alpaca':
        prompt_function = create_prompt_alpaca
    elif prompt_template == 'custom':
        prompt_function = create_prompt_custom
    elif prompt_template == 'gpt4':
        prompt_function = create_prompt_gpt4
    else:
        print(f'Invalid prompt template {prompt_template}')
        return

    model = GPT4All(model_name, ".")

    for i, question in enumerate(questions): 
        results = collection.query(query_texts=[question], n_results=2)
        print(results['distances'][0])
        dist_1, dist_2 = results['distances'][0]
        if abs(dist_1 - dist_2) / dist_1 < 0.15: 
            prompt = prompt_function(question, results['documents'][0])
        else:
            prompt = prompt_function(question, [results['documents'][0][0]])
        print(f"Question {i}")
        print(prompt)
        for o in model.generate(prompt, temp=temp, max_tokens=max_tokens, streaming=True):
            print(o, end="", flush=True)
        print('\n\n')


if __name__ == "__main__":
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
    args = parser.parse_args()
    print_args(args)

    main(args.model, args.temp, args.prompt_template, args.max_tokens)


