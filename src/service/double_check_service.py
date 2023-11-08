import os
import openai
import json

from util.logger import get_logger
from typing import List, Dict

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

openai.api_key = os.environ.get("OPENAI_API_KEY")
if openai.api_key is None:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")


class DoubleCheckService:
    def __init__(self, config: dict):
        self.config = config
        self.logger = get_logger(__name__, config)

    def double_check(self, analyzed_situation_with_law: List[Dict]) -> List[Dict]:
        # Für jede Aktion Artikel-Infos und Sachverhalt zusammentragen
        prompt_list = []
        analyzed_situation_with_law_and_double_checked = []
        for situation in analyzed_situation_with_law:
            for aktion in situation["aktionen"]:
                self.logger.info(f"aktion: {aktion}")
                artikel_infos = " ".join(
                    [
                        f"{artikel}: {text}"
                        for artikel, text in aktion["artikel"].items()
                    ]
                )

                aktion_ergebnis = f"Sachverhalt: {aktion['beschreibung']}\nArtikel-Infos: {artikel_infos}"
                prompt_list.append(aktion_ergebnis)

            count = 1

            for i in prompt_list:
                doublecheck_prompt = PromptTemplate(
                    input_variables=["situation_and_law"],
                    template="""\
                    Du bekommst die folgendenn Text mit einem Sacherhalt und Gesetzesartikeln {situation_and_law} mit der Artikel-Referenz und den Artikeltext. Prüfe welcher der Gesetzesartikel am besten zum Sachverhalt passt und liefere nur den diesen Artikel zurück und gib ein Objekt in folgender Struktur zurück wie folgt, ergänze keine Attribute:
                    "beschreibung": "Text von Sachverhalt", "artikel": Artikel als key:value pair, wobei der key der Artikel ist und der value der Text.
                        
                    Formatiere die Antwort in ein JSON.""",
                )
                llm = ChatOpenAI(
                    temperature=self.config["situation_analysis"]["temperature"],
                    model_name=self.config["situation_analysis"]["model_name"],
                )
                chain = LLMChain(
                    llm=llm,
                    prompt=doublecheck_prompt,
                    verbose=self.config["situation_analysis"]["verbose"],
                )

                output = chain.run(
                    {
                        "situation_and_law": i,
                    },
                )
                dict_output = json.loads(output)
                for aktion in situation["aktionen"]:
                    if aktion["id"] == count:
                        aktion["artikel"] = dict_output["artikel"]
                count += 1
            analyzed_situation_with_law_and_double_checked.append(situation)
        return analyzed_situation_with_law_and_double_checked
