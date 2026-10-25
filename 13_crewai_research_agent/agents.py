"""CrewAI agent definition."""

from crewai import Agent, LLM

from config import settings
from tools import db2_search_tool


llm = LLM(
    model=f"ollama/{settings.llm_model}",
    base_url=settings.ollama_base_url,
    temperature=0,
)


enterprise_researcher = Agent(
    role="Enterprise Researcher",
    goal=(
        "Answer enterprise knowledge questions using ONLY evidence retrieved "
        "from the IBM Db2 search tool. You must call the tool before "
        "answering. Never answer from memory or training data."
    ),
    backstory=(
        "You are an enterprise research assistant with access to an IBM Db2 "
        "knowledge base containing policies, incidents, architecture "
        "decisions, and technical documents. Your strict rule: you never "
        "state a fact about the enterprise without first retrieving it from "
        "the Db2 search tool. If the tool returns no relevant evidence you "
        "say so honestly rather than inventing an answer."
    ),
    tools=[db2_search_tool],
    llm=llm,
    verbose=True,
    max_iter=5,
    # Use the text-based ReAct executor so local Ollama models can emit
    # Thought/Action/Action Input steps that CrewAI actually dispatches.
    # The default structured executor requires native JSON tool-call output
    # which local models do not reliably produce.
    use_system_prompt=False,
)
