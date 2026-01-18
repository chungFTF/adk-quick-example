# System Architecture

## Multi-Agent System Overview

The Lifestyle Assistant is a Multi-Agent system built with Google ADK that coordinates three specialized agents to provide comprehensive lifestyle assistance.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                   User Query Input                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Lifestyle Coordinator (Root Agent)             │
│                  Type: SequentialAgent                      │
│                                                             │
│  Orchestrates sub-agents to process user queries and       │
│  provide comprehensive lifestyle assistance                │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌────────────────┐ ┌─────────────┐ ┌──────────────┐
│ Weather Agent  │ │ Restaurant  │ │ Event Agent  │
│                │ │ Agent       │ │              │
│ Type: LlmAgent │ │ Type:       │ │ Type:        │
│                │ │ LlmAgent    │ │ LlmAgent     │
├────────────────┤ ├─────────────┤ ├──────────────┤
│ Tools:         │ │ Tools:      │ │ Tools:       │
│ • google_      │ │ • get_      │ │ • search_    │
│   search       │ │   restaurant│ │   local_     │
│                │ │   _recom-   │ │   events     │
│                │ │   mendations│ │              │
├────────────────┤ ├─────────────┤ ├──────────────┤
│ Provides:      │ │ Provides:   │ │ Provides:    │
│ • Current      │ │ • Restaurant│ │ • Concerts   │
│   conditions   │ │   suggestions│ │ • Sports     │
│ • Forecasts    │ │ • Cuisine   │ │ • Theater    │
│ • Temperature  │ │   types     │ │ • Exhibitions│
│ • Precipitation│ │ • Budget    │ │ • Festivals  │
│                │ │   options   │ │              │
└────────────────┘ └─────────────┘ └──────────────┘
         │               │               │
         └───────────────┼───────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 Integrated Response                         │
│                                                             │
│  Combines results from all relevant agents into a          │
│  coherent, comprehensive answer                            │
└─────────────────────────────────────────────────────────────┘
```

## Agent Details

### 1. Lifestyle Coordinator (Root Agent)
- **Type**: SequentialAgent
- **Role**: Main orchestrator that routes queries to appropriate sub-agents
- **Processing**: Executes sub-agents sequentially
- **Output**: Integrated response from all relevant agents

### 2. Weather Agent
- **Type**: LlmAgent
- **Model**: gemini-2.5-flash
- **Tools**: google_search
- **Capabilities**:
  - Current weather conditions
  - Weather forecasts
  - Temperature information (Celsius and Fahrenheit)
  - Precipitation data
  - Weather alerts
- **State Output**: `weather_info`

### 3. Restaurant Agent
- **Type**: LlmAgent
- **Model**: gemini-2.5-flash-lite
- **Tools**: get_restaurant_recommendations (custom)
- **Capabilities**:
  - Cuisine-based recommendations
  - Budget filtering (budget-friendly, mid-range, fine-dining)
  - Location-based search
  - Dietary restriction support
  - Multiple recommendation options
- **State Output**: `restaurant_recommendations`

### 4. Event Agent
- **Type**: LlmAgent
- **Model**: gemini-2.5-flash-lite
- **Tools**: search_local_events (custom)
- **Capabilities**:
  - Concert discovery
  - Sports events
  - Theater shows
  - Art exhibitions
  - Festivals and community events
  - Date range filtering
  - Price filtering (free/ticketed)
- **State Output**: `event_info`

## Data Flow

1. **Query Reception**: User submits a query through the ADK web interface

2. **Root Agent Processing**: Lifestyle Coordinator receives the query

3. **Sequential Execution**:
   - **Weather Agent** processes the query:
     - If weather-related: Uses google_search to find information
     - If not relevant: Returns "not applicable" message
     - Stores results in state as `weather_info`
   
   - **Restaurant Agent** processes the query:
     - If dining-related: Uses get_restaurant_recommendations tool
     - Filters by cuisine, budget, dietary restrictions
     - Stores results in state as `restaurant_recommendations`
   
   - **Event Agent** processes the query:
     - If event-related: Uses search_local_events tool
     - Filters by category, date range, price
     - Stores results in state as `event_info`

4. **Response Integration**: Coordinator combines all relevant responses

5. **Output Delivery**: User receives comprehensive answer

## State Management

The system uses ADK's state management to share information:

```python
# Weather Agent
tool_context.state["weather_info"] = weather_data

# Restaurant Agent  
tool_context.state["restaurant_results"] = restaurant_data

# Event Agent
tool_context.state["event_results"] = event_data
```

Other agents and the root coordinator can access these states to provide integrated responses.

## Extension Points

The system can be extended with additional agents:

1. **Transportation Agent**: Public transit, rideshare, parking information
2. **Shopping Agent**: Store recommendations, deals, product searches
3. **Fitness Agent**: Gym recommendations, workout classes, outdoor activities
4. **Entertainment Agent**: Movies, streaming recommendations, game nights
5. **Travel Agent**: Hotels, flights, vacation planning

To add a new agent:
1. Create a new directory under `subagents/`
2. Implement the agent with appropriate tools
3. Add to root agent's `sub_agents` list
4. Update documentation

## Performance Considerations

- **Sequential Processing**: Agents execute in order, which may take longer for complex queries
- **Model Selection**: 
  - Use `gemini-2.5-flash` for tasks requiring Google Search or complex reasoning
  - Use `gemini-2.5-flash-lite` for lighter tasks with custom tools
- **Tool Optimization**: Custom tools use local data for fast responses

## Security & Privacy

- API keys stored in `.env` (never committed to version control)
- State management keeps data in memory during session
- No persistent storage of user queries or personal data
- All external API calls go through ADK's secure tool framework
