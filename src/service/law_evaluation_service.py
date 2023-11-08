import json
import os
import openai

from util.logger import get_logger
from typing import Tuple, List

from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

openai.api_key = os.environ.get("OPENAI_API_KEY")
if openai.api_key is None:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")


class LawEvaluationService:
    def __init__(self, config: dict):
        self.config = config
        self.logger = get_logger(__name__, config)

    def evaluate_laws(self, analyzed_situation_with_law: dict) -> List:
        action_list, article_dict = self.get_articles(analyzed_situation_with_law)
        format_instructions = self.get_format_instructions()
        violation_prompt_template = self.get_prompt_template()
        evaluated_articles = []

        for article_id, article_text in article_dict.items():
            evaluated_articles.append(
                self.enrich_article(
                    violation_prompt_template,
                    action_list,
                    article_text,
                    article_id,
                    format_instructions,
                )
            )

        self.logger.debug(evaluated_articles)

        return evaluated_articles

    def get_articles(self, analyzed_situation_with_law: dict) -> Tuple:
        action_list = ""
        article_dict = {}

        for aktion in analyzed_situation_with_law["aktionen"]:
            action_list += aktion["beschreibung"] + ", "

            for article_id, article_text in aktion["artikel"].items():
                if article_id not in article_dict:
                    article_dict[article_id] = article_text
        return action_list, article_dict

    def get_prompt_template(self) -> PromptTemplate:
        return PromptTemplate(
            input_variables=["aktionsliste", "artikel", "format_instructions"],
            template="""\
                Evaluiere anhand der folgenden kommaseparierten Liste von Aktionen ob die Person gegen den folgenden Gesetzesartikel verstösst des folgenden  ob die folgende aktion gegen ihn verstösst und \
                extrahiere die dazu folgenden Informationen: \

                Violation: Wurde gegen den Gesetzesartikel verstossen? Antworte True \
                wenn ja, oder antworte False wenn Nein oder es nicht klar ist.gegen den folgenden Gesetzesartikel '{artikel}' verstösst.",

                Reason: Begründe warum gegen den Gesetzesartikel verstossen wurde oder warum nicht.

                Aktionsliste: {aktionsliste}

                Artikel: {artikel}

                Formattiere die Antwort in ein valides JSON.

                {format_instructions}
            """,
        )

    def enrich_article(
        self,
        violation_prompt_template: PromptTemplate,
        action_list: str,
        article_text: str,
        article_id: str,
        format_instructions: str,
    ) -> dict:
        llm = ChatOpenAI(
            temperature=self.config["situation_analysis"]["temperature"],
            model_name=self.config["situation_analysis"]["model_name"],
        )

        chain = LLMChain(
            llm=llm,
            prompt=violation_prompt_template,
            verbose=self.config["situation_analysis"]["verbose"],
        )

        output = chain.run(
            {
                "aktionsliste": action_list,
                "artikel": article_text,
                "format_instructions": format_instructions,
            }
        )

        self.logger.debug(f"output: {output}")
        cleaned_output = output.replace("```json", "").replace("```", "")
        self.logger.debug(f"cleaned_output: {cleaned_output}")
        output_dict = json.loads(cleaned_output)
        output_dict["Article_ID"] = article_id
        output_dict["Article_Text"] = article_text
        return output_dict

    def get_format_instructions(self) -> str:
        self.logger.debug("get_format_instructions")
        violation_schema = ResponseSchema(
            name="violation",
            description="Wurde gegen den Gesetzesartikel verstossen? Antworte True wenn ja, oder antworte False wenn Nein oder es nicht klar ist.",
        )

        reason_schema = ResponseSchema(
            name="reason",
            description="Begründe warum gegen den Gesetzesartikel verstossen wurde oder warum nicht.",
        )

        response_schemas = [violation_schema, reason_schema]

        violation_output_parser = StructuredOutputParser.from_response_schemas(
            response_schemas
        )
        return violation_output_parser.get_format_instructions()
