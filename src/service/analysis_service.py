import os
import openai
import json
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from util.logger import get_logger

openai.api_key = os.environ.get("OPENAI_API_KEY")
if openai.api_key is None:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")


class AnalysisService:
    def __init__(self, config: dict):
        self.config = config
        self.logger = get_logger(__name__, config)
        self.prompt_template = PromptTemplate(
            input_variables=["concept"],
            template="""You're a traffic specialist app, that gets information for a traffic accident. This is what happend {concept}, return only a python dictionary for every involved party with the strict following structure, seperate every involved party with a |: 
            element 1 = "beteiligter": "Sample Name",element 2 "fahrzeug": "Vehicle", element 3"aktionen": as a list that contains max. 4 objects "id": 1, "beschreibung": "Sample Description,v max. 10 words per aktion""",
        )

    def analyze_incident(self, situation_text: str) -> dict:
        self.logger.debug(f"Create OpenAI model with config: {self.config['situation_analysis']}")
        llm = ChatOpenAI(
            temperature=self.config["situation_analysis"]["temperature"],
            model_name=self.config["situation_analysis"]["model_name"],
        )
        self.logger.debug(f'Set concept to {situation_text}')
        self.prompt_template.format(concept=situation_text)
        chain = LLMChain(llm=llm, prompt=self.prompt_template, verbose=self.config['situation_analysis']["verbose"])

        self.logger.debug(f'Run chain with situation: {situation_text}')
        output = chain.run(situation_text)
        self.logger.debug(f'Chain output: {output}')
        if "|" not in output:
            # todo retry?
            self.logger.error(
                f"Chain output does not contain expected separator '|': {output}"
            )
            raise ValueError("Output does not contain expected separator '|'")

        splitted_list = output.split("|")
        dict_list = [json.loads(s) for s in splitted_list]

        return {"result": dict_list}
