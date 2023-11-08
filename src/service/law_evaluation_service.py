import json
import os
import openai
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from util.logger import get_logger

openai.api_key = os.environ.get("OPENAI_API_KEY")
if openai.api_key is None:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")


class LawEvaluationService:
    def __init__(self, config: dict):
        self.config = config
        self.logger = get_logger(__name__, config)

    def evaluate_law(self, input: dict) -> list:
        action_list = ''
        article_dict = {}

        for aktion in input['aktionen']:
            action_list += aktion['beschreibung'] + ', '

            for article_id, article_text in aktion['artikel'].items():
                if article_id not in article_dict:
                    article_dict[article_id] = article_text

        violation_schema = ResponseSchema(name='violation',
                                          description='Wurde gegen den Gesetzesartikel verstossen? \
                                     Antworte True wenn ja, oder antworte False wenn Nein oder es nicht klar ist.')

        reason_schema = ResponseSchema(name='reason',
                                       description='Begründe warum gegen den Gesetzesartikel \
                                     verstossen wurde oder warum nicht.')

        response_schemas = [violation_schema,
                            reason_schema]

        violation_output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

        # format_instructions = violation_output_parser.get_format_instructions()

        violation_prompt_template = PromptTemplate(
            input_variables=['aktionsliste', 'artikel'],
            template="""\
                Evaluiere anhand der folgenden kommaseparierten Liste von Aktionen ob die Person gegen den folgenden Gesetzesartikel verstösst des folgenden  ob die folgende aktion gegen ihn verstösst und \
                extrahiere die dazu folgenden Informationen: \

                Violation: Wurde gegen den Gesetzesartikel verstossen? Antworte True \
                wenn ja, oder antworte False wenn Nein oder es nicht klar ist.gegen den folgenden Gesetzesartikel '{artikel}' verstösst.",

                Reason: Begründe warum gegen den Gesetzesartikel verstossen wurde oder warum nicht.

                Aktionsliste: {aktionsliste}

                Artikel: {artikel}

                Formattiere die Antwort in ein valides JSON.
            """
        )

        evaluated_articles = []

        for article_id, article_text in article_dict.items():
            prompt = violation_prompt_template.format(aktionsliste=action_list, artikel=article_text)

            llm = ChatOpenAI(temperature=0.0, model_name="gpt-3.5-turbo")
            chain = LLMChain(llm=llm, prompt=violation_prompt_template, verbose=True)

            output = chain.run({'aktionsliste': action_list, 'artikel': article_text}, )

            output_dict = json.loads(output)
            output_dict['Article_ID'] = article_id

            evaluated_articles.append(output_dict)

        self.logger.debug(evaluated_articles)

        return evaluated_articles
