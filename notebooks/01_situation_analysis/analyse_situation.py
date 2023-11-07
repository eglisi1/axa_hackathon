from dotenv import load_dotenv
import os
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Load the environment variables from the .env file
load_dotenv()

# Now you can use os.getenv to access your variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
 
# Text-Input
situation = "B1 fuhr mit einem Personenwagen und B2 mit ihrem eBike von Ittigen herkommend auf der Papiermühlestrasse in Richtung stadteinwärts. Bei der Lichtsignalanlage Papiermühle-/Worblaufenstrasse blinkte B1 nach eigenen Angaben nach rechts, machte den Seitenblick und bog folglich im Schritttempo nach rechts in Richtung Worblaufenstrasse ab, als B2 zur selben Zeit weiter geradeaus fuhr. B2 bemerkte zu spät, dass B1 rechts abbog, woraufhin B2 mit dem Vorderrad ihres eBikes in die Hintere rechte Fahrzeugseite von B1 prallte und folglich zu Boden fiel. "
 
# Step 4: Define the Prompt Template
prompt = PromptTemplate(
    input_variables=["concept"],
    template= "You're a technical user, that gets a course of event for a traffic accident. There are two involved parties. This is what happend {concept} Create a dictionary with the following structure: Beteiligter': '1',Fahrzeug': '', 'Behaviour step 1': '', 'Behaviour step 2': '', 'Behaviour step n': ' 'Beteiligter': '2', 'Fahrzeug': '', 'Behaviour step 1': '', 'Behaviour step 2': '', 'Behaviour step n' : ''",
)
 
# Step 5: Print the Prompt Template
print(prompt.format(concept=situation))
 
# Step 6: Instantiate the LLMChain
llm = OpenAI(temperature=0.9)
chain = LLMChain(llm=llm, prompt=prompt, verbose = True)
print(f'hi {chain}')
 
# Step 7: Run the LLMChain
output = chain.run(situation)
print(output)






