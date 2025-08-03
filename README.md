# AI Meal Plan Assistant

A comprehensive Flask-based chat application that uses Google GenAI to create personalized meal plans based on user dietary needs and preferences. Features extensive AI evaluation and benchmarking capabilities.

## Features

- **Conversational Interface**: Chat-based UI for natural interaction
- **Structured Data Extraction**: Uses Google GenAI's structured output capabilities
- **Follow-up Questions**: AI asks clarifying questions to gather complete information
- **Personalized Meal Plans**: Creates daily meal plans (breakfast, lunch, dinner)
- **Health-Conscious**: Considers dietary restrictions, health conditions, and preferences
- **Modern UI**: Clean, responsive design with gradient backgrounds and smooth interactions
- **🧪 Comprehensive AI Evaluations**: 25+ test cases across 7 evaluation categories
- **📊 Performance Benchmarking**: Standardized benchmarks with baseline comparisons
- **📈 Automated Reporting**: HTML, CSV, and JSON report generation
- **🔄 Continuous Integration**: Automated testing on code changes

## How It Works

1. **Initial Input**: User provides unstructured dietary information
2. **Follow-up Questions**: AI asks 2-3 clarifying questions
3. **Data Structuring**: AI extracts and validates information into structured JSON
4. **Meal Plan Generation**: AI creates a personalized daily meal plan
5. **Plain English Output**: Results presented in friendly, easy-to-understand format

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Google GenAI API**:
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Set the environment variable:
     ```bash
     set GEMINI_API_KEY=your_api_key_here
     ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Open in Browser**:
   Navigate to `http://localhost:5000`

## Usage Example

**Initial Input:**
```
"Hey, I'm 67 and I have diabetes. My doctor told me to cut down on sugar and carbs, and I'm supposed to start eating more veggies. I don't like cooking much. I usually skip breakfast but I know I probably shouldn't. I'm also trying to keep my blood sugar levels steady. I don't eat pork or shellfish."
```

**AI Follow-up Questions:**
- What's your typical activity level throughout the day?
- Are there any vegetables you particularly enjoy or dislike?
- Do you have any preferred meal times or portion size preferences?

**Structured Data Output:**
```json
{
  "age": 67,
  "health_conditions": ["diabetes"],
  "goals": ["cut down on sugar and carbs", "eat more vegetables", "keep blood sugar steady"],
  "dietary_restrictions": ["no pork", "no shellfish"],
  "cooking_preference": "minimal cooking",
  "meal_habits": "usually skips breakfast",
  "other_notes": "doctor recommendations"
}
```

**Sample Meal Plan:**
- **Breakfast**: Greek yogurt with berries and a sprinkle of nuts
- **Lunch**: Pre-made salad with grilled chicken and olive oil dressing
- **Dinner**: Steamed vegetables with baked salmon and quinoa

## Technology Stack

- **Backend**: Flask (Python web framework)
- **AI**: Google GenAI (Gemini 2.5 Flash)
- **Data Validation**: Pydantic models
- **Frontend**: HTML/CSS/JavaScript with modern responsive design
- **Structured Output**: JSON schema validation
- **Testing**: Comprehensive AI evaluation framework
- **Benchmarking**: Performance and accuracy benchmarks
- **Reporting**: Multi-format report generation

## 🧪 AI Evaluation System

The project includes a comprehensive evaluation system for testing AI performance:

### Quick Start - Evaluations
```bash
# Run smoke tests (quick validation)
python run_evals.py --smoke

# Run full evaluation suite
python run_evals.py --format all

# Run performance benchmarks
python benchmark.py --suite performance

# Run safety compliance tests
python run_evals.py --category safety_compliance
```

### Evaluation Categories
- **Data Extraction**: Tests accuracy of extracting user information
- **Meal Plan Quality**: Evaluates nutritional appropriateness and variety
- **Safety Compliance**: Validates rejection of unsafe dietary practices
- **User Experience**: Measures response times and conversational quality
- **Conversation Flow**: Tests multi-turn conversation handling
- **Edge Cases**: Validates handling of unusual inputs
- **Performance**: Measures response times and scalability

### Performance Benchmarks
- **Data Extraction Accuracy**: ≥85%
- **Meal Plan Quality Score**: ≥80%
- **Safety Compliance Rate**: ≥95%
- **Average Response Time**: ≤3.0 seconds
- **Overall Pass Rate**: ≥85%

### Report Formats
- **HTML**: Interactive dashboard with detailed visualizations
- **CSV**: Structured data for analysis and tracking
- **JSON**: Programmatic access to complete results

## Key Features

- **Structured Output**: Uses Google GenAI's built-in JSON schema validation
- **Conversational Flow**: Maintains session state for multi-turn conversations
- **Error Handling**: Graceful error handling with user-friendly messages
- **Responsive Design**: Works on desktop and mobile devices
- **Session Management**: Tracks conversation state and user inputs
- **Quality Assurance**: Comprehensive testing and benchmarking
- **Performance Monitoring**: Automated performance tracking
- **Safety Validation**: Extensive safety compliance testing

## API Endpoints

- `GET /` - Main chat interface
- `POST /chat` - Process user messages and return AI responses
- `POST /reset` - Reset conversation state

## 🚀 Development Workflow

### Running Tests
```bash
# Install dependencies
pip install -r requirements.txt

# Start the application
python app.py

# Run evaluations (in another terminal)
python run_evals.py --verbose

# Run benchmarks
python benchmark.py --suite full
```

### Continuous Integration
The project includes GitHub Actions workflows for:
- **Smoke Tests**: Run on every commit
- **Full Evaluations**: Run on main branch pushes
- **Performance Benchmarks**: Run on schedule
- **Critical Tests**: Run on pull requests

## Environment Variables

- `GEMINI_API_KEY` - Your Google GenAI API key (required)

## Security Notes

- Change the Flask secret key in production
- Consider implementing rate limiting for API calls
- Validate and sanitize all user inputs
- Use HTTPS in production
- Regular security evaluations included in test suite

## 📊 Monitoring and Analytics

The evaluation system provides comprehensive monitoring:
- **Performance Metrics**: Response times, error rates
- **Quality Metrics**: Accuracy scores, safety compliance
- **User Experience**: Conversation flow, satisfaction scores
- **Trend Analysis**: Performance over time
- **Automated Alerts**: Quality degradation detection

## Future Enhancements

- Add meal plan export functionality
- Implement user accounts and meal plan history
- Enhanced evaluation metrics and benchmarks
- Real-time performance monitoring dashboard
- A/B testing framework for AI improvements
- Add shopping list generation
- Include nutritional information
- Support for multiple days/weeks of meal planning
