import yaml
import pandas as pd
import os
import itertools

import pinecone

from sentence_transformers import SentenceTransformer

with open("../../src/config/cfg.yaml", "r") as stream:
    config = yaml.safe_load(stream)

api_key = os.environ.get("PINECONE_API_KEY")
if api_key is None:
    raise ValueError("The PINECONE_API_KEY environment variable is not set.")


def main():
    index_name = "law"
    df = load_dataset()
    df = vectorize(df)
    amount_dimensions = len(df["vectors"][0])
    pinecone.init(api_key=api_key, environment=config["vectorization"]["environment"])
    delete_existing_index(index_name)
    index = create_index(index_name, amount_dimensions)
    # Convert DataFrame to a list of tuples (id, vector, metadata)
    to_upsert = df.apply(lambda x: (x['id'], x['vectors'].tolist(), {"text": x['Text']}), axis=1).tolist()
    
    # Upsert data with 5 vectors per upsert request
    for ids_vectors_chunk in chunks(to_upsert, batch_size=5):
        index.upsert(vectors=ids_vectors_chunk)  # Assuming `index` defined elsewhere


def load_dataset() -> pd.DataFrame:
    df = pd.read_csv("../../data/02_interim/law/law_art_abs_text.csv", delimiter="|")
    df["id"] = (
        df["Gesetz"].astype(str)
        + "_"
        + df["Artikel"].astype(str)
        + "_"
        + df["Absatz"].astype(str)
    )
    return df


def vectorize(df: pd.DataFrame) -> pd.DataFrame:
    model = SentenceTransformer(config["sentence_transformer"]["model_name"])
    df["vectors"] = df["Text"].apply(lambda x: model.encode(x))
    return df


def delete_existing_index(index_name: str) -> None:
    if index_name in pinecone.list_indexes():
        pinecone.delete_index(index_name)
        print(f"Deleted index {index_name}.")


def create_index(index_name: str, amount_dimensions: int) -> pinecone.Index:
    pinecone.create_index(
        index_name,
        dimension=amount_dimensions,
        metric=config["vectorization"]["metric"],
    )
    pinecone.describe_index(index_name)
    return pinecone.Index(index_name)

def chunks(iterable, batch_size=100):
    """A helper function to break an iterable into chunks of size batch_size."""
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))

if __name__ == "__main__":
    main()
