# Lifestyle Assistant Multi-Agent System

A sophisticated Multi-Agent system built with Google ADK that helps users with daily lifestyle queries including weather information, restaurant recommendations, and local event discovery.

## System Architecture

![System Workflow](Workflow.png)

## Directory Structure

```
adk-lifestyle-assistant/
├── .env.example                    # Environment configuration example
├── README.md                       # This documentation
└── lifestyle_coordinator/          # Root agent
    ├── __init__.py
    ├── agent.py                    # Main agent definition
    └── subagents/                  # Sub-agents directory
        ├── __init__.py
        ├── weather_agent/          # Weather information agent
        │   ├── __init__.py
        │   └── agent.py
        ├── restaurant_agent/       # Restaurant recommendation agent
        │   ├── __init__.py
        │   ├── agent.py
        │   └── tools.py
        └── event_agent/            # Event discovery agent
            ├── __init__.py
            ├── agent.py
            └── tools.py
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
pip install google-adk
```

## Launch and Usage

### 1. Authentication Setup (Vertex AI Users Only)

If you selected "Vertex AI" in the environment setup, authenticate with Google Cloud:

```bash
gcloud auth application-default login
```

**Note**: Skip this step if you're using "Google AI Studio".

### 2. Start Dev UI

Navigate to the adk-lifestyle-assistant directory:

```bash
cd adk-lifestyle-assistant
```

Run the following command to start the Dev UI:

```bash
adk web
```

### 3. Open Web Interface

Open the provided URL in your browser (usually `http://localhost:8000`), and select `lifestyle_coordinator` from the dropdown in the top-left corner.

## System Features

### Root Coordinator

**Lifestyle Coordinator** is the core controller of the system, using a `SequentialAgent` architecture to orchestrate all sub-agents' workflows.

### Sub-Agent Details

#### 1. Weather Agent

**File Location**: `lifestyle_coordinator/subagents/weather_agent/agent.py`

**Features**:
- Provides current weather conditions and forecasts
- Uses Google Search tool to find up-to-date weather information
- Handles location-based queries

**Capabilities**:
- Current weather conditions
- Weather forecasts
- Temperature, precipitation, and wind information
- Location-specific weather data

#### 2. Restaurant Agent

**File Location**: `lifestyle_coordinator/subagents/restaurant_agent/agent.py`

**Features**:
- Recommends restaurants based on user preferences
- Considers cuisine type, price range, and location
- Provides detailed restaurant information

**Main Functions**:
- `get_restaurant_recommendations` tool
- Cuisine-based filtering
- Budget-conscious recommendations

**Recommendation Logic**:
1. Analyze user preferences (cuisine, budget, location)
2. Search for matching restaurants
3. Provide detailed recommendations with ratings and reviews
4. Consider dietary restrictions and special requirements

#### 3. Event Agent

**File Location**: `lifestyle_coordinator/subagents/event_agent/agent.py`

**Features**:
- Discovers local events and activities
- Searches for concerts, exhibitions, sports events, and more
- Provides event details including time, location, and tickets

**Main Functions**:
- `search_local_events` tool
- Category-based event filtering
- Date and location-based search

**Search Capabilities**:
- Cultural events (concerts, theater, exhibitions)
- Sports events
- Community activities
- Entertainment and nightlife
- Family-friendly events

## Usage Examples

**Query**: "What's the weather like today and where should I eat dinner?"

**System Execution Flow**:
1. **Weather Agent** searches for current weather information
2. **Restaurant Agent** recommends suitable dining options
3. **Lifestyle Coordinator** integrates both responses into a coherent answer

**Query**: "Find me a good Italian restaurant and check if there are any concerts this weekend"

**System Execution Flow**:
1. **Restaurant Agent** searches for Italian restaurants
2. **Event Agent** discovers weekend concerts
3. **Lifestyle Coordinator** presents a comprehensive response with dining and entertainment options

## System Highlights

### 1. Intelligent Query Routing
- All agents have smart routing mechanisms
- Can identify and categorize different types of user queries
- Appropriately rejects or redirects irrelevant questions

### 2. Multi-Layer Architecture Design
- **Sequential**: Ensures orderly workflow execution
- **Parallel**: Improves system execution efficiency (when needed)
- **Modular**: Easy to extend with additional agents

### 3. Flexible Tool Integration
- Google Search for real-time information
- Custom tools for specific domain queries
- Extensible tool framework

### 4. Multi-Domain Integration
- Combines weather data
- Integrates restaurant information
- Discovers local events
- Provides comprehensive lifestyle assistance

## Technical Architecture

### Agent Types

1. **SequentialAgent**: Executes sub-agents in order
2. **ParallelAgent**: Executes sub-agents concurrently
3. **LlmAgent**: Single agent based on Large Language Models

### State Management

ADK provides a robust state management system that enables effective information sharing between agents:

#### **State Setting and Reading**
- **State in Tools**: Use `tool_context.state` in tool functions to set or read state
- **Agent Output State**: Agent's `output_key` is also a form of state setting
- **Cross-Agent Sharing**: Different agents can share information through the state mechanism

#### **State Propagation Flow**
1. **State Creation or Update**: Agents create or update relevant state information during execution
2. **State Reading**: Subsequent agents can read previously set state to achieve information transfer
3. **Error Feedback**: For example, query failures can be recorded in state for iteration

#### **Practical Examples**
- **Weather State**: Weather Agent results available to other agents
- **Restaurant Preferences**: User preferences shared across agents
- **Event Results**: Event Agent findings accessible to Coordinator

### Model Usage

- **gemini-2.5-flash**: Used for complex reasoning and search tasks
- **gemini-2.5-flash-lite**: Used for lighter analysis and summary tasks
- **Model Extensibility**: Beyond Gemini models, you can integrate other models (like GPT, Claude) through LiteLLM
  - 📖 Detailed Guide: [LiteLLM and Google ADK Integration](https://docs.litellm.ai/docs/tutorials/google_adk)

### Tool Integration

- **google_search**: Web search functionality for real-time information
- **get_restaurant_recommendations**: Restaurant search and filtering
- **search_local_events**: Event discovery and details

## Frequently Asked Questions

### Q: Can I add more agents to the system?
A: 
- Yes, the system is designed to be modular and extensible
- Simply create a new agent in the `subagents/` directory
- Add it to the root agent's sub_agents list
- Follow the existing agent patterns

### Q: How does the system handle multiple queries in one request?
A: 
- The Lifestyle Coordinator processes queries sequentially
- Each relevant agent handles its domain
- Results are integrated into a comprehensive response

### Q: Can I customize the restaurant or event recommendations?
A: 
- Yes, you can modify the tools in each agent
- Add custom filters and preferences
- Integrate with external APIs for more data sources

### Q: What if a query doesn't match any agent's domain?
A: 
- The Coordinator will analyze the query
- Provide a helpful response indicating the system's capabilities
- Suggest alternative queries that the system can handle

## Next Steps

After completing the Lifestyle Assistant tutorial, you can:

1. Extend the system with additional agents (transportation, shopping, fitness, etc.)
2. Learn how to deploy ADK agents as web applications
3. Study how to integrate different data sources and APIs
4. Develop domain-specific multi-agent systems for your use cases
