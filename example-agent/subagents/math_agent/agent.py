"""
Math Agent
Performs mathematical calculations and solves math problems
"""

from google.adk.agents import Agent

GEMINI_MODEL = "gemini-2.5-flash"

math_agent = Agent(
    name="math_agent",
    # model to use for the agent
    model=GEMINI_MODEL,
    description="Math calculation agent that performs arithmetic and solves math problems",
    # instruction for the agent
    instruction="""
    You are a math calculation assistant.
    
    You can help with:
    - Basic arithmetic (addition, subtraction, multiplication, division)
    - Percentages and ratios
    - Averages and statistics
    
    Show your work step-by-step and provide clear answers.
    """,
    tools=[],
    output_key="math_result"
)
