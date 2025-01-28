import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import AIMessage
load_dotenv()

idea_generator_prompt = PromptTemplate.from_template(
    "You are an expert in reviewing research literature and identifying research gaps and opportunities. "
    "You are given a topic and you are to generate a list of potential research directions on the topic. "
    "Just respond with a list of 5 research directions, and a short explanation for each, no other text. "
    "The topic is: {topic}"
)

idea_refiner_prompt = PromptTemplate.from_template(
    "You are an expert in reviewing research literature and identifying research gaps and opportunities. "
    "You are given a topic and you are to generate a list of potential research directions on the topic and feedback on the previous list of research directions. "
    "The topic is: {topic}"
    "The previous list of research directions is: {ideas}"
    "You were given feedback on your previous list of research directions. "
    "The feedback is: {feedback}"
    "Just respond with the refined research directions, incorporating the feedback into each one of them."
    "You should provide a roadmap for each research direction, including things like what data you need, what methods you need to use, etc."
    "The previous few refined lists are: {messages}"
)

evaluator_prompt = PromptTemplate.from_template(
    "You are an expert in evaluating research ideas."
    "Given a list of research ideas, you are to evaluate them and pick which ones are the most promising."
    "You need to make sure that the ideas are not too similar to each other, and that they are not too broad."
    """The purpose is to identify the most promising research ideas according to feasibility, novelty, impact, 
    or required resources, and refine them into a more detailed research plan later."""
    """The topic is: {topic} and the list of research ideas is: 
    {ideas}"""
    "Just respond with your feedback on the list of research ideas, no other text. Mention what is good and what is bad about the ideas."
)

generator = idea_generator_prompt | ChatOpenAI(
    model="o1-mini") | StrOutputParser()

refiner = idea_refiner_prompt | ChatOpenAI(
    model="o1-mini") | StrOutputParser()

evaluator = evaluator_prompt | ChatOpenAI(
    model="gpt-4o") | StrOutputParser()

ROUNDS = 3
TOPIC = "herbarium specimen identification"  # TODO: IDEALLY, ASK USER FOR TOPIC

ideas = generator.invoke(
    {"topic": TOPIC})

print("="*100)
print(f"FIRST IDEAS: \n{ideas}")
print("="*100)

messages = [AIMessage(content=ideas)]

for i in range(ROUNDS):
    print("*"*100)
    print(f"Starting Round {i+1}")
    feedback = evaluator.invoke(
        {"topic": TOPIC, "ideas": ideas})
    print(f"Feedback: \n{feedback}")
    print("-"*50)
    ideas = refiner.invoke(
        {"topic": TOPIC, "feedback": feedback, "ideas": ideas, "messages": messages[-3:]})
    print(f"Refined Ideas: \n{ideas}")
    print("*"*100)
    messages.append(AIMessage(content=ideas))

print("="*100)
print(f"FINAL IDEAS: \n {ideas}")
print("="*100)
