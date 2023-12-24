## Assistant

Simple proof of concept chatbot using open-source LLMs which answers queries from a custom text-based database.


### Running
Add your `.txt` files inside the `database` folder. Also add their metadata (i.e. tags) inside the `metadata` folder.
All `database` files must have a correspondent `metadata` file. Right now the `metadata` data isn't used for anything,
but it may be used to improve semantic search results.

Then install (Usage of a virtual environment is recommended)
```
pip3 install -r requirements.txt
```

To run the CLI interface run
```
python3 main.py -m <model-path>
```
For the web interface run

```
python3 app.py -m <model-path>
```

Check the available options

```
python3 app.py --help # or main.py --help
```

### Dependencies
This repo depends on [GPT4All](https://github.com/nomic-ai/gpt4all/) and [chromadb](https://github.com/chroma-core/chroma). If
you wish to run the web chatbot you will also need [Flask](https://github.com/pallets/flask/), [Flask-Socket](https://github.com/miguelgrinberg/flask-socketio) and [Deep Translator](https://github.com/nidhaloff/deep-translator) (If you wish to use the chatbot in a language other than english). The JS frontend also references the `socket.io` lib for websockets stuff.


### Models
GPT4All accepts `.gguf` files. The chatbot performance will be directly impacted by your LLM model choice.
[TheBloke](https://huggingface.co/TheBloke) has many models that you can download. A few lightweight models that 
I recommend are `nous-hermes-llama2-13b.Q4_0.gguf`, `mistral-7b-instruct-v0.1.Q4_0.gguf` and `openchat_3.5.Q5_K_M.gguf`.
Note that these models may sometimes hallucinate when the semantic search yields poor results. Improving the 
semantic search procedure will improve the overall model's performance.
