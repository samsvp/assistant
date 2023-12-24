import os
import ast
import chromadb


def create_collection(database_folder: str) -> chromadb.Collection:
    client = chromadb.Client()
 
    collection = client.create_collection("docs")
      
    metadatas = []
    documents = []
    ids = []
    for file in os.listdir(database_folder):
        with open(os.path.join(database_folder, file)) as fp:
            doc = fp.read()
        with open(os.path.join("metadata", file)) as fp:
            meta = ast.literal_eval(fp.read())
        ids.append(file.rsplit(".")[0])
        documents.append(doc)
        metadatas.append(meta)
    
     
    collection.add(
        documents=documents, 
        metadatas=metadatas, 
        ids=ids,
    )
    
    return collection


if __name__ == "__main__":
    collection = create_collection("database")
    with open("test-questions/questions.txt") as fp:
        questions = fp.read()
     
    for question in questions.split("\n")[:-1]:
        print("Question:", question)
        results = collection.query(
            query_texts=[question],
            n_results=2,
            # where={"metadata_field": "is_equal_to_this"}, # optional filter
            # where_document={"$contains":"search_string"}  # optional filter
        )
        print(results)
        print()
     
