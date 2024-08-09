from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = OpenAI(temperature=0.5)

# Define a prompt template for generating a topic
topic_template = PromptTemplate.from_template(
    "Name a random topic in one word.")

# Define a prompt template for generating a joke
joke_template = PromptTemplate(
    input_variables=["topic"],
    template="Tell me a funny joke about {topic}."
)

topic_chain = topic_template | llm | StrOutputParser()

joke_chain = joke_template | llm

topic = topic_chain.invoke({})
print(topic)

joke = joke_chain.invoke(topic)
print(joke)

# Output:
# Bananas
# Why did the banana go to the doctor? Because it wasn't peeling well!
