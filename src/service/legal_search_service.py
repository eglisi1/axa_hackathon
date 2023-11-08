from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import pinecone
from langchain.vectorstores import Pinecone
import pandas as pd

from util.logger import get_logger
from features.preprocess import remove_stopwords, lemmatize

import openai
import os
from typing import List, Dict

openai.api_key = os.environ.get("OPENAI_API_KEY")
if openai.api_key is None:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

pinecone_api_key = os.environ.get("PINECONE_API_KEY")
if pinecone_api_key is None:
    raise ValueError("The PINECONE_API_KEY environment variable is not set.")


class LegalSearchService:
    def __init__(self, config: dict):
        self.config = config
        self.logger = get_logger(__name__, config)
        self.text_field = "text"
        self.__init_pinecone__()
        self.embed = HuggingFaceEmbeddings(
            model_name=self.config["sentence_transformer"]["model_name"]
        )
        self.__load_vectorstore__()

    def __init_pinecone__(self):
        pinecone.init(
            api_key=pinecone_api_key,
            environment=self.config["vectorization"]["environment"],
        )
        index_name_law = "law"
        self.index = pinecone.Index(index_name_law)

    def __load_vectorstore__(self):
        self.vectorstore = Pinecone(
            self.index, self.embed.embed_query, text_key=self.text_field
        )

    def search_relevant_articles(self, analyzed_situation: List[Dict]) -> List[Dict]:
        for situation in analyzed_situation:
            self.logger.debug(f"Situation: {situation}")
            for action in situation["aktionen"]:
                self.logger.debug(f"Action: {action}")
                query = self.create_query(action["beschreibung"])
                documents = self.vectorstore.similarity_search(query, k=5)
                self.logger.debug(f"Documents: {documents}")
                artikel = {}
                # TODO: Implement threshold
                for document in documents:
                    print(type(document))
                    self.logger.debug(f"Document: {document}")
                    key, original_text = self.load_original_text_with_key(document.page_content)
                    self.logger.debug(f"Key: {key}, Original Text: {original_text}")
                    artikel[key] = original_text
                action["artikel"] = artikel
        self.logger.debug(f"Return: {analyzed_situation}")
        return analyzed_situation

    def create_query(self, query_text) -> str:
        query = query_text
        self.logger.debug(f"Original query: {query}")
        query = remove_stopwords(query)
        query = lemmatize(query)
        self.logger.debug(f"Preprocessed query: {query}")
        return query

    def load_original_text_with_key(self, preprocessed_text: str) -> [str, str]:
        # TODO: dont open the file every time
        self.logger.debug(f"Preprocessed text: {preprocessed_text}")
        df_interim = pd.read_csv(
            "../data/02_interim/law/law_art_abs_text.csv", delimiter="|"
        )
        filtered_df = df_interim[df_interim["Text"] == preprocessed_text]
        merged_column = (
            filtered_df["Gesetz"]
            + " "
            + filtered_df["Artikel"]
            + " "
            + filtered_df["Absatz"]
        )
        key = merged_column.values[0]
        self.logger.debug(f"Key: {key}")
        gesetz = filtered_df["Gesetz"].iloc[0]
        artikel = filtered_df["Artikel"].iloc[0]
        absatz = filtered_df["Absatz"].iloc[0]
        df_original = pd.read_csv(
            "../data/01_raw/law/law_art_abs_text.csv", delimiter="|"
        )
        filtered_df = df_original[
            (df_original["Gesetz"] == gesetz)
            & (df_original["Artikel"] == artikel)
            & (df_original["Absatz"] == absatz)
        ]
        original_text = filtered_df["Text"].iloc[0]
        self.logger.debug(f"Original text: {original_text}")
        return key, original_text
