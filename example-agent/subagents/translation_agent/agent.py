"""
Translation Agent
Provides language translation and language learning assistance
"""

from google.adk.agents import Agent

GEMINI_MODEL = "gemini-2.5-flash-lite"

translation_agent = Agent(
    name="translation_agent",
    model=GEMINI_MODEL,
    description="Translation agent that translates between languages and helps with language learning",
    instruction="""
    You are a translation and language assistant.
    
    You can help with:
    - Translating text between languages
    - Explaining word meanings and usage
    - Providing pronunciation guidance
    - Teaching common phrases
    - Explaining cultural context
    
    Provide accurate translations and helpful language learning tips.
    """,
    tools=[],
    output_key="translation_result"
)
