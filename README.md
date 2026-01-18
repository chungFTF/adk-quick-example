# Example Agent Multi-Agent System

A Multi-Agent system built with Google ADK that demonstrates intelligent query routing to specialized agents for mathematical calculations and language translation tasks.

## System Architecture

For detailed architecture information, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Directory Structure

```
adk-example/
├── .env.example                    # Environment configuration example
├── README.md                       # This documentation
├── ARCHITECTURE.md                 # System architecture details
├── QUICK_START.md                  # Quick start guide
├── TESTING_GUIDE.md                # Testing instructions
├── requirements.txt                # Python dependencies
└── example-agent/                  # Root agent
    ├── __init__.py
    ├── agent.py                    # Main agent definition
    └── subagents/                  # Sub-agents directory
        ├── __init__.py
        ├── math_agent/             # Math calculation agent
        │   ├── __init__.py
        │   └── agent.py
        └── translation_agent/      # Translation agent
            ├── __init__.py
            └── agent.py
```

## Environment Setup

### 1. Configure Environment Variables

First, copy the `.env.example` file and rename it to `.env`:

```bash
cp .env.example .env
```

Then choose one of the following configuration options:

#### Option 1: Using Vertex AI
```env
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-east5
```

#### Option 2: Using Google AI API
```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your-api-key
```

⚠️ **Important**: Do not commit real API keys to version control.

### 2. Install Dependencies

Ensure you have the required Python packages installed:

```bash
pip install -r requirements.txt
```

Or install directly:

```bash
pip install google-adk python-dotenv
```

## Launch and Usage

### 1. Authentication Setup (Vertex AI Users Only)

If you selected "Vertex AI" in the environment setup, authenticate with Google Cloud:

```bash
gcloud auth application-default login
```

**Note**: Skip this step if you're using "Google AI Studio".

### 2. Start Dev UI

Navigate to the adk-example directory:

```bash
cd adk-example
```

Run the following command to start the Dev UI:

```bash
adk web
```

### 3. Open Web Interface

Open the provided URL in your browser (usually `http://localhost:8000`), and select `root_agent` from the dropdown in the top-left corner.

## System Features

### Root Coordinator

**Root Agent** is the intelligent coordinator that analyzes user queries and routes them to the appropriate specialized agent based on query type.

### Sub-Agent Details

#### 1. Math Agent

**File Location**: `example-agent/subagents/math_agent/agent.py`

**Features**:
- Performs mathematical calculations and solves math problems
- Provides step-by-step solutions
- Handles various types of mathematical queries

**Capabilities**:
- Basic arithmetic (addition, subtraction, multiplication, division)
- Percentages and ratios
- Averages and statistics
- Step-by-step problem solving with clear explanations

**Model**: gemini-2.5-flash

**Output Key**: `math_result`

#### 2. Translation Agent

**File Location**: `example-agent/subagents/translation_agent/agent.py`

**Features**:
- Provides language translation and language learning assistance
- Explains word meanings and usage
- Helps with cultural context

**Capabilities**:
- Translating text between languages
- Explaining word meanings and usage
- Teaching common phrases
- Explaining cultural context

**Model**: gemini-2.5-flash-lite

**Output Key**: `translation_result`

## Usage Examples

**Query**: "What is 25% of 480?"

**System Execution Flow**:
1. **Root Agent** analyzes the query and identifies it as a math question
2. Routes the query to **Math Agent**
3. **Math Agent** calculates the answer: 120
4. Provides step-by-step explanation: 25% = 0.25, so 0.25 × 480 = 120

**Query**: "Translate 'Hello, how are you?' to Spanish"

**System Execution Flow**:
1. **Root Agent** analyzes the query and identifies it as a translation question
2. Routes the query to **Translation Agent**
3. **Translation Agent** provides the translation: "Hola, ¿cómo estás?"
4. May also provide additional context or variations

**Query**: "Calculate the average of 10, 20, 30, 40, 50 and translate the result to French"

**System Execution Flow**:
1. **Root Agent** identifies this as a multi-part query
2. Routes to **Math Agent** first to calculate average: (10+20+30+40+50)/5 = 30
3. Routes to **Translation Agent** to translate "30" to French: "trente"
4. Provides integrated response with both results

## System Highlights

### 1. Intelligent Query Routing
- Root agent analyzes queries and identifies their type
- Automatically routes to the most appropriate specialized agent
- Provides helpful responses for queries outside system capabilities

### 2. Modular Architecture Design
- **Modular**: Easy to extend with additional agents
- **Specialized**: Each agent focuses on its domain expertise
- **Flexible**: Agents can be added or modified independently

### 3. Model Optimization
- Uses appropriate models for different task complexities
- `gemini-2.5-flash` for complex reasoning (root agent, math agent)
- `gemini-2.5-flash-lite` for lighter tasks (translation agent)

### 4. State Management
- Agents use `output_key` to store results in state
- Root coordinator can access agent outputs for integrated responses
- Enables information sharing between agents when needed

## Technical Architecture

### Agent Types

The system uses ADK's `Agent` class for all agents:
- **Root Agent**: Routes queries to sub-agents
- **Math Agent**: Handles mathematical calculations
- **Translation Agent**: Handles language translation

### State Management

ADK provides a robust state management system that enables effective information sharing between agents:

#### **State Setting and Reading**
- **Agent Output State**: Agent's `output_key` stores results in state
- **Cross-Agent Sharing**: Root coordinator can access sub-agent outputs
- **State Access**: Results stored with keys like `math_result` and `translation_result`

#### **State Propagation Flow**
1. **Query Routing**: Root agent routes query to appropriate sub-agent
2. **Agent Execution**: Sub-agent processes query and stores result in state
3. **Result Access**: Root agent can access stored results for integrated responses

#### **Practical Examples**
- **Math Results**: Math Agent stores calculation results in `math_result`
- **Translation Results**: Translation Agent stores translations in `translation_result`
- **Coordinator Access**: Root agent can access both for multi-part queries

### Model Usage

- **gemini-2.5-flash**: Used for complex reasoning tasks (root agent, math agent)
- **gemini-2.5-flash-lite**: Used for lighter tasks (translation agent)
- **Model Extensibility**: Beyond Gemini models, you can integrate other models (like GPT, Claude) through LiteLLM
  - 📖 Detailed Guide: [LiteLLM and Google ADK Integration](https://docs.litellm.ai/docs/tutorials/google_adk)

### Tool Integration

Currently, both sub-agents rely on model capabilities without external tools. The system can be extended with:
- Custom tools for specific calculations
- External translation APIs
- Database lookups
- API integrations

## Frequently Asked Questions

### Q: Can I add more agents to the system?
A: 
- Yes, the system is designed to be modular and extensible
- Simply create a new agent in the `example-agent/subagents/` directory
- Add it to the root agent's `sub_agents` list in `example-agent/agent.py`
- Update the root agent's instruction to include routing logic for the new agent
- Follow the existing agent patterns

### Q: How does the system handle queries that don't match any agent?
A: 
- The Root Agent analyzes the query
- If it doesn't match math or translation categories, it provides a helpful response
- Explains what the system can assist with
- Suggests alternative queries that the system can handle

### Q: Can I customize the agents' capabilities?
A: 
- Yes, you can modify the instructions in each agent's definition
- Add custom tools to agents if needed
- Adjust model selection based on task complexity
- Extend capabilities by adding new tools or modifying instructions

### Q: How do I add tools to an agent?
A: 
- Define tool functions using ADK's tool decorator
- Add tools to the agent's `tools` parameter
- Tools can access `tool_context.state` for state management
- See ADK documentation for detailed tool implementation examples

## Next Steps

After exploring this example agent system, you can:

1. Extend the system with additional agents (code generation, writing, research, etc.)
2. Add custom tools to agents for specific functionality
3. Learn how to deploy ADK agents as web applications
4. Study how to integrate different data sources and APIs
5. Develop domain-specific multi-agent systems for your use cases

## Additional Resources

- [ARCHITECTURE.md](ARCHITECTURE.md) - Detailed system architecture
- [QUICK_START.md](QUICK_START.md) - Quick start guide
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Testing instructions
- [Google ADK Documentation](https://ai.google.dev/adk)
