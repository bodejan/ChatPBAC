from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(temperature=0.5)

# Define a prompt template for generating a joke
prompt_template = PromptTemplate(
    input_variables=["topic"],
    template="Tell me a funny joke about {topic}."
)

joke_chain = prompt_template | llm

print(prompt_template.format_prompt(topic="cats"))

print(joke_chain.invoke("cats"))

# Output:
# text='Tell me a funny joke about cats.'
# Why was the cat sitting on the computer? Because it wanted to keep an eye on the mouse!
