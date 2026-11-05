import os
from dotenv import load_dotenv

import crewai.llms.cache as crewai_cache
crewai_cache.mark_cache_breakpoint = lambda msg: msg

from crewai import Agent, LLM

load_dotenv()

llm = LLM(
    model="groq/openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2
)

discovery_agent = Agent(
    role="Research Paper Discovery Agent",
    goal="Find and organize relevant academic papers.",
    backstory="You are an academic research expert.",
    llm=llm,
    verbose=True
)

summarization_agent = Agent(
    role="Research Paper Summarization Agent",
    goal="Summarize research papers accurately.",
    backstory="You are an expert in academic paper summarization.",
    llm=llm,
    verbose=True
)

literature_agent = Agent(
    role="Literature Review Agent",
    goal="Compare research methodologies and findings.",
    backstory="You are an academic literature review specialist.",
    llm=llm,
    verbose=True
)

gap_agent = Agent(
    role="Research Gap Agent",
    goal="Identify research gaps and limitations.",
    backstory="You are a research gap identification expert.",
    llm=llm,
    verbose=True
)

report_agent = Agent(
    role="Research Report Agent",
    goal="Generate a complete academic research report.",
    backstory="You are a professional academic report writer.",
    llm=llm,
    verbose=True
)