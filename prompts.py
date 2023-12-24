from typing import Tuple


def create_prompt_custom(question: str, context: Tuple[str, str]) -> str:
    return f"""
    You are at Miramar Hotel. Answer the question choosing one of the following data. Discard the data which you didn't use: 
    ### DATA 1: {context[0]}
    ### DATA 2: {context[1]}
    ### QUESTION: {question}
    ### RESPONSE:
    """


def create_prompt_alpaca(question: str, context: Tuple[str, str]) -> str:
    data = ''.join(context)
    return f"""
    You are at Miramar Hotel. Below is an instruction that describes a task. Write a short response that appropriately completes the request based on the following information: {data}
    ### QUESTION: {question}
    ### RESPONSE:
    """

def create_prompt_gpt4(question: str, context: Tuple[str, str]) -> str:
    data = ''.join(context)
    return f"""
    You are at Miramar Hotel. Below is an instruction that describes a task. Write a short response that appropriately completes the request based on the following information: {data}
    User: {question}<|end_of_turn|>GPT4 Assistant:
    """
