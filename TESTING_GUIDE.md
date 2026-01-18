# Testing Guide

This guide provides test scenarios and expected behaviors for the Lifestyle Assistant Multi-Agent System.

## Prerequisites

Before testing, ensure:
1. You've completed the setup in `QUICK_START.md`
2. The ADK web interface is running (`adk web`)
3. `lifestyle_coordinator` is selected in the agent dropdown

## Test Scenarios

### 1. Weather Agent Tests

#### Test 1.1: Basic Weather Query
**Input**: "What's the weather in New York today?"

**Expected Behavior**:
- Weather Agent activates and uses google_search
- Returns current weather conditions for New York
- Other agents respond with "not applicable" messages

#### Test 1.2: Weather Forecast Query
**Input**: "Will it rain in San Francisco this weekend?"

**Expected Behavior**:
- Weather Agent searches for SF weekend forecast
- Provides precipitation information
- Includes both current conditions and forecast

#### Test 1.3: Non-Weather Query
**Input**: "What's the best Italian restaurant?"

**Expected Behavior**:
- Weather Agent responds: "This query is not related to weather information"
- Restaurant Agent provides recommendations
- Event Agent responds: "not applicable"

---

### 2. Restaurant Agent Tests

#### Test 2.1: Basic Restaurant Query
**Input**: "Find me a good Italian restaurant"

**Expected Behavior**:
- Restaurant Agent uses get_restaurant_recommendations tool
- Returns 1-2 Italian restaurants
- Includes details: name, location, price range, specialties

**Example Output**:
```
Restaurant Recommendations:

1. Bella Vista (Downtown)
   - Budget: Mid-range
   - Specialties: Carbonara, Margherita Pizza, Tiramisu
   - Features: Outdoor seating, Wine bar, Romantic atmosphere
   - Dietary Options: Vegetarian, Gluten-free

2. Trattoria del Porto (Waterfront)
   - Budget: Fine-dining
   - Specialties: Seafood Risotto, Osso Buco, Panna Cotta
   - Features: Ocean view, Reservations required
```

#### Test 2.2: Budget-Specific Query
**Input**: "I need a budget-friendly Chinese restaurant"

**Expected Behavior**:
- Restaurant Agent filters by cuisine (Chinese) and budget (budget-friendly)
- Returns Golden Dragon
- Highlights budget-friendly features

#### Test 2.3: Dietary Restriction Query
**Input**: "Recommend a vegetarian Japanese restaurant"

**Expected Behavior**:
- Restaurant Agent filters for Japanese cuisine with vegetarian options
- Returns restaurants that support dietary restrictions
- Mentions vegetarian-friendly dishes

#### Test 2.4: Fine Dining Query
**Input**: "I want a fine dining experience"

**Expected Behavior**:
- Restaurant Agent searches for fine-dining options
- May present options from multiple cuisines
- Emphasizes upscale features and price ranges

---

### 3. Event Agent Tests

#### Test 3.1: Concert Search
**Input**: "What concerts are happening this weekend?"

**Expected Behavior**:
- Event Agent uses search_local_events with category="concerts"
- Returns upcoming concerts within the weekend date range
- Includes date, time, venue, price information

**Example Output**:
```
Upcoming Concerts:

1. Jazz Night at The Blue Room
   - Date: January 18, 2026 at 8:00 PM
   - Location: The Blue Room, Downtown
   - Price: $25-40
   - Features: Bar available, 21+, Reservations recommended

2. Summer Symphony Concert Series
   - Date: January 20, 2026 at 7:00 PM
   - Location: City Park Amphitheater
   - Price: Free
   - Features: Outdoor venue, Family-friendly
```

#### Test 3.2: Free Events Query
**Input**: "Are there any free events this week?"

**Expected Behavior**:
- Event Agent filters by price_filter="free"
- Returns all free events within the week
- Includes various categories (concerts, festivals, exhibitions, sports)

#### Test 3.3: Sports Events Query
**Input**: "Find me sports events today"

**Expected Behavior**:
- Event Agent searches category="sports" with date_range="today"
- Returns sports events scheduled for today
- If none today, states "no events found"

#### Test 3.4: Theater Shows Query
**Input**: "What theater shows are playing this month?"

**Expected Behavior**:
- Event Agent searches category="theater" with date_range="this_month"
- Returns theater performances
- Includes show details and ticket information

---

### 4. Multi-Domain Tests

#### Test 4.1: Weather + Restaurant
**Input**: "What's the weather like and where should I eat dinner?"

**Expected Behavior**:
- Weather Agent provides current weather conditions
- Restaurant Agent suggests dinner options
- Event Agent responds: "not applicable"
- Coordinator integrates both responses

#### Test 4.2: Restaurant + Events
**Input**: "I need an Italian restaurant and want to know about concerts this weekend"

**Expected Behavior**:
- Weather Agent: "not applicable"
- Restaurant Agent provides Italian restaurant recommendations
- Event Agent lists weekend concerts
- Comprehensive response with both dining and entertainment options

#### Test 4.3: All Three Domains
**Input**: "What's the weather for Saturday, recommend a good restaurant, and are there any events?"

**Expected Behavior**:
- Weather Agent provides Saturday forecast
- Restaurant Agent suggests restaurants
- Event Agent lists available events
- Fully integrated response covering all three areas

#### Test 4.4: Unrelated Query
**Input**: "Help me write a Python function"

**Expected Behavior**:
- All agents respond with "not applicable" messages
- System politely indicates it specializes in lifestyle assistance
- May suggest the types of queries it can handle

---

### 5. Edge Cases

#### Test 5.1: Vague Query
**Input**: "I'm bored"

**Expected Behavior**:
- Agents may ask for clarification
- Event Agent might suggest browsing available events
- System should guide user to provide more specific requests

#### Test 5.2: Location-Specific Multi-Query
**Input**: "I'm visiting Chicago - what's the weather, where should I eat, and what events are happening?"

**Expected Behavior**:
- Weather Agent searches Chicago weather
- Restaurant Agent provides Chicago restaurant recommendations
- Event Agent lists Chicago events
- All responses contextualized to Chicago

#### Test 5.3: Impossible Request
**Input**: "Find me a free Michelin-star restaurant"

**Expected Behavior**:
- Restaurant Agent acknowledges the constraint conflict
- Suggests alternatives (e.g., fine-dining options or free but high-quality restaurants)
- Provides helpful guidance

---

## Validation Checklist

After each test, verify:

- [ ] Appropriate agents responded to their domain
- [ ] Non-relevant agents gracefully declined
- [ ] Response is coherent and helpful
- [ ] Information is accurate and relevant
- [ ] State management working (data shared between agents if needed)
- [ ] No errors in console or UI
- [ ] Response time is reasonable (< 30 seconds typically)

## Common Issues and Solutions

### Issue 1: All Agents Responding "Not Applicable"
**Cause**: Query not matching any agent's instruction patterns
**Solution**: Rephrase query to be more specific about weather/restaurants/events

### Issue 2: Weather Agent Not Finding Results
**Cause**: Google Search may require specific formatting
**Solution**: Include location explicitly in query

### Issue 3: Restaurant Agent Returns Empty Results
**Cause**: No restaurants match exact criteria in sample database
**Solution**: 
- Try different cuisine types (Italian, Chinese, Japanese, Mexican)
- Adjust budget constraints
- Check `restaurant_agent/tools.py` for available restaurants

### Issue 4: Event Agent Returns "No Results"
**Cause**: Sample events may not match exact date range
**Solution**:
- Try broader date ranges ("this week" instead of "today")
- Check `event_agent/tools.py` for sample event dates
- Use different event categories

### Issue 5: Slow Response Time
**Cause**: Google Search can take time for external queries
**Solution**: This is expected for weather queries using google_search

---

## Extending Tests

To add custom test data:

1. **Add Restaurants**: Edit `lifestyle_coordinator/subagents/restaurant_agent/tools.py`
   - Add new cuisine types or restaurants to the `restaurants` dictionary

2. **Add Events**: Edit `lifestyle_coordinator/subagents/event_agent/tools.py`
   - Add new events to the `events` dictionary
   - Update dates to current/future dates

3. **Modify Agent Behavior**: Edit each agent's `agent.py` file
   - Adjust instructions for different response styles
   - Modify relevance checking logic

---

## Performance Benchmarks

Expected response times (approximate):

| Query Type | Expected Time | Notes |
|------------|---------------|-------|
| Weather only | 5-15 seconds | Depends on google_search |
| Restaurant only | 2-5 seconds | Uses local data |
| Events only | 2-5 seconds | Uses local data |
| Multi-domain | 10-20 seconds | Sequential processing |

---

## Reporting Issues

If you encounter unexpected behavior:

1. Check the console for error messages
2. Verify your `.env` configuration
3. Ensure all dependencies are installed
4. Check that you're using compatible ADK version
5. Review agent instructions for relevance matching

---

## Advanced Testing

### Testing State Management

To verify state is being shared between agents:

1. Enable debug logging in ADK
2. Check `tool_context.state` contents after each agent execution
3. Verify state keys: `weather_info`, `restaurant_results`, `event_results`

### Testing with Different Models

Try switching models in agent files:
- `gemini-2.5-flash` - More capable, slower, better for complex reasoning
- `gemini-2.5-flash-lite` - Faster, good for structured tasks
- Compare response quality and speed

### Load Testing

Test system performance with rapid consecutive queries to understand:
- Response consistency
- State management reliability
- Resource usage

---

## Success Criteria

A successful test run should demonstrate:

✅ All agents correctly identify relevant queries  
✅ Non-relevant queries are gracefully handled  
✅ Tools are called with correct parameters  
✅ Responses are accurate and helpful  
✅ Multi-domain queries are properly integrated  
✅ System maintains good performance  
✅ Error handling works appropriately
