import os
import openai
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

openai.api_key = os.environ['OPENAI_API_KEY']

input = {
    "beteiligter": "Beteiligter 1",
    "fahrzeug": "Ford Fiesta",
    "aktionen": [
        {
            "id": 1,
            "beschreibung": "Hat rechts abgebogen",
            "artikel_id": "VRV 28 1",
            "artikel_text": "Der Fahrzeugführer hat alle Richtungsänderungen anzukündigen, auch das Abbiegen nach rechts. Selbst der Radfahrer, der zum Überholen eines andern ausschwenkt, hat dies anzuzeigen."
        },
        {
            "id": 2,
            "beschreibung": "Hat nicht geblinkt",
            "artikel_id": "VRV 17 5",
            "artikel_text": "Kündigt der Führer eines Busses im Linienverkehr innerorts bei einer gekennzeichneten Haltestelle mit den Richtungsblinkern an, dass er wegfahren will, so müssen die von hinten herannahenden Fahrzeugführer nötigenfalls die Geschwindigkeit mässigen oder halten, um ihm die Wegfahrt zu ermöglichen; dies gilt nicht, wenn sich die Haltestelle am linken Fahrbahnrand befindet. Der Busführer darf die Richtungsblinker erst betätigen, wenn er zur Wegfahrt bereit ist; er muss warten, wenn von hinten herannahende Fahrzeuge nicht rechtzeitig halten können."
        }
    ]
}

violation_prompt_template = PromptTemplate(
    input_variables=['aktion', 'artikel'],
    template="Sag mir ob die Aktion '{aktion}' gegen den folgenden Gesetzesartikel '{artikel}' verstösst."
)

for aktion in input["aktionen"]:
    prompt = violation_prompt_template.format(aktion=aktion["beschreibung"], artikel=aktion['artikel_text'])

    print(prompt)

    llm = ChatOpenAI(temperature=0.0, model_name="gpt-3.5-turbo")
    chain = LLMChain(llm=llm, prompt=violation_prompt_template, verbose=True)

    output = chain.run({'aktion': aktion["beschreibung"], 'artikel': aktion['artikel_text']})
    print("\nAntwort: " +" "+ output)
