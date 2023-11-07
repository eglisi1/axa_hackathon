
import os
import openai
import json
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


# Now you can use os.getenv to access your variables
openai.api_key  = os.environ['OPENAI_API_KEY']
 
# Text-Input
situation = "G kam über die Obere Zollgasse her gefharen, weiter in Richtung Ostermundigen. Auf Höhe der Verzweigung Waldheimstrasse kam gleichzeitig B über die Waldheimstrasse her gefahren und wollte nach rechts in die Obere Zollgasse einbiegen. B missachtete dabei den Vortritt und kollidierte so mit seiner linken Fahrzeugfront mit der rechten Fahrzeugseite von G."
 
# Step 4: Define the Prompt Template
prompt = PromptTemplate(
    input_variables=["concept"],
    template= """You're a traffic specialist app, that gets information for a traffic accident. This is what happend {concept}, return only a python dictionary for every involved party with the strict following structure, seperate the objects with a |: 
    element 1 = "beteiligter": "Sample Name",element 2 "fahrzeug": "Sample Vehicle", element 3"aktionen": as a list that contains max. 4 objects "id": 1, "beschreibung": "Sample Description,v max. 10 words per aktion""",
)
 
# Step 5: Print the Prompt Template
print(prompt.format(concept=situation))
 
# Step 6: Instantiate the LLMChain
llm = OpenAI(temperature=0.2, model_name="gpt-3.5-turbo")
chain = LLMChain(llm=llm, prompt=prompt, verbose = True)
 
# Step 7: Run the LLMChain
output = chain.run(situation)
print("Chain-Output" +" "+ output)

splitted_list = output.split('|')
print("splittet_list") 
print(splitted_list)

# Wandeln Sie jeden String in der Liste in ein Dictionary um
dict_list = [json.loads(s) for s in splitted_list]

# dict_list ist nun eine Liste von Dictionaries
print("dict_list") 
print(dict_list)

dict_list[0]






