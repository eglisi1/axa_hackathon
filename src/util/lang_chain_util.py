import os
import openai

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from util.config import load_config

config = load_config("config/cfg.yaml")

openai.api_key = os.environ.get("OPENAI_API_KEY")
if openai.api_key is None:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")


def create_llm() -> ChatOpenAI:
    return ChatOpenAI(
        temperature=config["situation_analysis"]["temperature"],
        model_name=config["situation_analysis"]["model_name"],
    )


def create_llm_chain(llm, prompt) -> LLMChain:
    return LLMChain(llm, prompt=prompt, verbose=config["situation_analysis"]["verbose"])
