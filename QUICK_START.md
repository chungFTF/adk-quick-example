# Quick Start Guide

## Prerequisites

- Python 3.10 or higher
- Google Cloud Project (for Vertex AI) or Google AI API key

## Installation

1. **Clone or navigate to the repository:**
   ```bash
   cd adk-lifestyle-assistant
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` with your credentials:
   - For Vertex AI: Set `GOOGLE_GENAI_USE_VERTEXAI=TRUE` and configure project details
   - For Google AI: Set `GOOGLE_GENAI_USE_VERTEXAI=FALSE` and add your API key

4. **Authenticate (Vertex AI only):**
   ```bash
   gcloud auth application-default login
   ```

5. **Launch the application:**
   ```bash
   adk web
   ```

6. **Access the UI:**
   - Open your browser to `http://localhost:8000`
   - Select `lifestyle_coordinator` from the agent dropdown

## Example Queries

Try these queries to test the system:

### Weather Queries
- "What's the weather like in San Francisco today?"
- "Will it rain this weekend in New York?"
- "Show me the weather forecast for Tokyo"

### Restaurant Queries
- "Find me a good Italian restaurant for dinner"
- "I want budget-friendly Chinese food downtown"
- "Recommend a fine dining Japanese restaurant"

### Event Queries
- "What concerts are happening this weekend?"
- "Are there any free events this week?"
- "Find me sports events today"

### Combined Queries
- "What's the weather like and where should I eat dinner?"
- "I need restaurant recommendations and any events happening this weekend"

## Architecture Overview

The system uses a Sequential Agent architecture:

```
Lifestyle Coordinator (Root)
  ├── Weather Agent (Google Search)
  ├── Restaurant Agent (Custom Tool)
  └── Event Agent (Custom Tool)
```

Each agent processes queries in order, but only responds to relevant queries within its domain.

## Troubleshooting

### Common Issues

1. **Import errors:**
   - Ensure you're in the correct directory when running `adk web`
   - Verify all dependencies are installed

2. **Authentication errors:**
   - For Vertex AI: Run `gcloud auth application-default login`
   - For Google AI: Check your API key in `.env`

3. **Agent not found:**
   - Make sure you're running `adk web` from the `adk-lifestyle-assistant` directory
   - Check that all `__init__.py` files are present

## Next Steps

- Customize agent instructions in each agent's `agent.py` file
- Add more restaurants to the database in `restaurant_agent/tools.py`
- Add more events to the database in `event_agent/tools.py`
- Extend the system with additional agents (transportation, shopping, fitness, etc.)

## Support

For ADK documentation and tutorials, visit:
- [Google ADK Documentation](https://ai.google.dev/adk)
- [ADK GitHub Repository](https://github.com/google/adk)
