"""
Multi-Agent Coordinator - Root Agent
Intelligently routes user queries to appropriate specialized agents
"""

from google.adk.agents import Agent
from google.genai import types

from .subagents.math_agent import math_agent
from .subagents.translation_agent import translation_agent

GEMINI_MODEL = "gemini-2.5-flash"

# Root Agent with intelligent routing
# Analyzes user queries and routes to the appropriate specialized agent
root_agent = Agent(
    name="root_agent",

    # model to use for the agent
    model=GEMINI_MODEL,
    # description of the agent
    description="Multi-agent coordinator that intelligently routes queries to specialized agents",
    # instruction for the agent
    instruction="""
    You are an intelligent coordinator that routes user queries to specialized agents.
    
    Analyze user queries and route to the appropriate agent:
    - Math questions (calculations, arithmetic, percentages, algebra) → math_agent
    - Translation questions (language translation, word meanings, phrases) → translation_agent
    
    Route the query to the most appropriate agent. If the query doesn't fit either category,
    provide a helpful response explaining what you can assist with.
    """,
    # sub-agents to use for the agent
    sub_agents=[math_agent, translation_agent]
)
