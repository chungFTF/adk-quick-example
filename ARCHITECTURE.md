# System Architecture

## Multi-Agent System Overview

The Example Agent is a Multi-Agent system built with Google ADK that coordinates two specialized agents to handle mathematical calculations and language translation tasks.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                   User Query Input                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Root Agent (Coordinator)                       │
│                  Type: Agent                                │
│                                                             │
│  Intelligently routes user queries to specialized agents    │
│  based on query type (math or translation)                 │
└────────────────────────┬────────────────────────────────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
┌─────────────────────┐  ┌──────────────────────┐
│   Math Agent        │  │  Translation Agent   │
│                     │  │                      │
│ Type: Agent         │  │ Type: Agent          │
│ Model: gemini-2.5-  │  │ Model: gemini-2.5-  │
│       flash         │  │       flash-lite     │
├─────────────────────┤  ├──────────────────────┤
│ Capabilities:      │  │ Capabilities:        │
│ • Basic arithmetic │  │ • Language           │
│ • Percentages      │  │   translation       │
│ • Ratios           │  │ • Word meanings     │
│ • Averages         │  │ • Common phrases    │
│ • Statistics       │  │ • Cultural context  │
├─────────────────────┤  ├──────────────────────┤
│ Output Key:        │  │ Output Key:         │
│ math_result        │  │ translation_result  │
└─────────────────────┘  └──────────────────────┘
              │                     │
              └──────────┬───────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 Integrated Response                         │
│                                                             │
│  Returns result from the appropriate specialized agent     │
└─────────────────────────────────────────────────────────────┘
```

## Agent Details

### 1. Root Agent (Coordinator)
- **Type**: Agent
- **Model**: gemini-2.5-flash
- **Role**: Intelligent coordinator that routes queries to appropriate sub-agents
- **Routing Logic**:
  - Math questions (calculations, arithmetic, percentages, algebra) → math_agent
  - Translation questions (language translation, word meanings, phrases) → translation_agent
- **Sub-agents**: [math_agent, translation_agent]

### 2. Math Agent
- **Type**: Agent
- **Model**: gemini-2.5-flash
- **Capabilities**:
  - Basic arithmetic (addition, subtraction, multiplication, division)
  - Percentages and ratios
  - Averages and statistics
  - Step-by-step problem solving
- **Output Key**: `math_result`
- **Tools**: None (uses model's built-in math capabilities)

### 3. Translation Agent
- **Type**: Agent
- **Model**: gemini-2.5-flash-lite
- **Capabilities**:
  - Translating text between languages
  - Explaining word meanings and usage
  - Teaching common phrases
  - Explaining cultural context
- **Output Key**: `translation_result`
- **Tools**: None (uses model's built-in translation capabilities)

## Data Flow

1. **Query Reception**: User submits a query through the ADK web interface

2. **Root Agent Processing**: Root agent receives the query and analyzes it

3. **Query Routing**: 
   - Root agent determines if the query is:
     - **Math-related**: Routes to math_agent
     - **Translation-related**: Routes to translation_agent
     - **Neither**: Provides helpful response explaining capabilities

4. **Agent Execution**:
   - **Math Agent** (if routed):
     - Processes mathematical query
     - Shows work step-by-step
     - Stores result in state as `math_result`
   
   - **Translation Agent** (if routed):
     - Processes translation or language query
     - Provides translation or explanation
     - Stores result in state as `translation_result`

5. **Response Delivery**: User receives answer from the appropriate specialized agent

## State Management

The system uses ADK's state management to share information:

```python
# Math Agent
output_key="math_result"  # Stores math calculation results

# Translation Agent
output_key="translation_result"  # Stores translation results
```

The root coordinator can access these output states to provide integrated responses when needed.

## Extension Points

The system can be extended with additional agents:

1. **Code Agent**: Code generation, debugging, code explanation
2. **Writing Agent**: Content creation, editing, proofreading
3. **Research Agent**: Information gathering, fact-checking
4. **Analysis Agent**: Data analysis, chart generation
5. **Conversation Agent**: General conversation, Q&A

To add a new agent:
1. Create a new directory under `example-agent/subagents/`
2. Implement the agent with appropriate model and instructions
3. Add to root agent's `sub_agents` list in `example-agent/agent.py`
4. Update routing logic in root agent's instruction
5. Update documentation

## Performance Considerations

- **Model Selection**: 
  - Use `gemini-2.5-flash` for complex reasoning tasks (root agent, math agent)
  - Use `gemini-2.5-flash-lite` for lighter tasks (translation agent)
- **Routing Efficiency**: Root agent quickly identifies query type and routes to appropriate agent
- **No External Tools**: Both sub-agents rely on model capabilities, ensuring fast responses

## Security & Privacy

- API keys stored in `.env` (never committed to version control)
- State management keeps data in memory during session
- No persistent storage of user queries or personal data
- All processing done through ADK's secure framework
