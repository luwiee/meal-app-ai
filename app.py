from flask import Flask, render_template, request, jsonify, session
import os
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import List, Optional
import json
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Initialize Google GenAI client
try:
    client = genai.Client(api_key="AIzaSyAFUd1RFT5RGOSwbI6bWhB-8RjUOdWmwN4")
except Exception as e:
    print(f"Error initializing Google GenAI client: {e}")
    client = None

class MealPlanData(BaseModel):
    age: Optional[int] = None
    health_conditions: List[str] = []
    goals: List[str] = []
    dietary_restrictions: List[str] = []
    likes: List[str] = []
    dislikes: List[str] = []
    cooking_preference: Optional[str] = None
    meal_habits: Optional[str] = None
    other_notes: Optional[str] = None

class FollowUpQuestions(BaseModel):
    questions: List[str]
    
class MealPlan(BaseModel):
    breakfast: str
    lunch: str
    dinner: str
    key_decisions: str

class RejectedInfo(BaseModel):
    rejected_items: List[str]
    reasons: List[str]

class AIResponse(BaseModel):
    step: str
    follow_up_questions: Optional[List[str]] = None
    structured_data: Optional[MealPlanData] = None
    meal_plan: Optional[MealPlan] = None
    rejected_info: Optional[RejectedInfo] = None
    explanation: Optional[str] = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if client is None:
        return jsonify({
            'type': 'error',
            'message': 'AI service is not available. Please check the API key configuration.'
        })
    
    user_message = request.json.get('message', '')
    
    if 'conversation_state' not in session:
        session['conversation_state'] = 'initial'
        session['collected_info'] = ''
        session['question_count'] = 0
        session['conversation_id'] = str(uuid.uuid4())
    
    try:
        if session['conversation_state'] == 'initial':
            # Store the initial input and ask first follow-up question
            session['collected_info'] = user_message
            session['conversation_state'] = 'follow_up'
            session['question_count'] = 0
            
            # Generate the first follow-up question
            return generate_next_question()
            
        elif session['conversation_state'] == 'follow_up':
            # Add the user's answer to collected info
            session['collected_info'] += f" {user_message}"
            session['question_count'] += 1
            
            # Check if we should ask another question or generate meal plan
            if session['question_count'] >= 3:
                # Force meal plan generation after 3 questions
                return generate_meal_plan_response()
            else:
                # Let the API decide whether to ask another question or proceed
                return generate_next_question()
                
        else:
            # Reset conversation
            session['conversation_state'] = 'initial'
            session['collected_info'] = ''
            session['question_count'] = 0
            return jsonify({
                'type': 'reset',
                'message': 'Let\'s start fresh! Please share your dietary needs and preferences.'
            })
            
    except Exception as e:
        return jsonify({
            'type': 'error',
            'message': f'Sorry, I encountered an error: {str(e)}'
        })

def generate_next_question():
    try:
        questions_asked = session['question_count']
        collected_info = session['collected_info']
        
        # Create a decision prompt for the AI
        prompt = f"""
        You are an AI Meal Plan Assistant. You have collected this information from the user:
        
        "{collected_info}"
        
        You have already asked {questions_asked} follow-up questions. You can ask up to 3 total questions.
        
        Analyze the information and decide:
        1. If you have enough information to create a good meal plan, respond with: "PROCEED_TO_MEAL_PLAN"
        2. If you need more information (and haven't reached 3 questions yet), ask ONE specific follow-up question
        
        Focus on missing critical information like:
        - Specific dietary restrictions not mentioned
        - Activity level or portion preferences  
        - Specific food preferences or cooking constraints
        - Meal timing preferences
        - Allergies or intolerances
        
        If asking a question, respond with just the question (no extra text).
        If proceeding to meal plan, respond with exactly: "PROCEED_TO_MEAL_PLAN"
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            )
        )
        
        ai_response = response.text.strip()
        print(f"AI decision: {ai_response}")  # Debug print
        
        if ai_response == "PROCEED_TO_MEAL_PLAN":
            return generate_meal_plan_response()
        else:
            # AI wants to ask another question
            return jsonify({
                'type': 'single_question',
                'question': ai_response,
                'message': ai_response
            })
    
    except Exception as e:
        print(f"Error generating next question: {e}")
        # Fallback: ask a default question or proceed to meal plan
        if session['question_count'] < 2:
            default_questions = [
                "What vegetables do you enjoy most, and are there any you particularly dislike?",
                "Do you have any other dietary restrictions or food allergies I should know about?",
                "What are your preferred meal times and portion sizes?"
            ]
            question = default_questions[session['question_count']]
            return jsonify({
                'type': 'single_question',
                'question': question,
                'message': question
            })
        else:
            return generate_meal_plan_response()

def generate_meal_plan_response():
    # Use all collected information
    all_inputs = session['collected_info']
    
    # Step 2: Structure the data and identify rejected information
    structured_data, rejected_info = extract_structured_data(all_inputs)
    
    # Step 3: Generate meal plan
    meal_plan = generate_meal_plan(structured_data, all_inputs)
    
    # Reset conversation state
    session['conversation_state'] = 'complete'
    
    response_data = {
        'type': 'meal_plan',
        'structured_data': structured_data,
        'meal_plan': meal_plan,
        'message': 'Here\'s your personalized daily meal plan!'
    }
    
    # Add rejected info if any exists
    if rejected_info and (rejected_info.get('rejected_items') or rejected_info.get('reasons')):
        response_data['rejected_info'] = rejected_info
    
    return jsonify(response_data)

def extract_structured_data(user_input):
    # First, extract structured data
    structured_prompt = f"""
    Extract and structure the following user input into a JSON object. Be precise and only include information that is explicitly stated or strongly implied.
    
    User Input: "{user_input}"
    
    Extract into this exact JSON structure:
    {{
        "age": number or null,
        "health_conditions": [list of strings],
        "goals": [list of strings],
        "dietary_restrictions": [list of strings],
        "likes": [list of strings],
        "dislikes": [list of strings],
        "cooking_preference": string or null,
        "meal_habits": string or null,
        "other_notes": string or null
    }}
    
    Be conservative - if something is unclear or not mentioned, use null or empty arrays.
    """
    
    structured_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=structured_prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": MealPlanData,
            "thinking_config": {"thinking_budget": 0}
        }
    )
    
    structured_data = structured_response.parsed.__dict__
    
    # Now identify rejected/ignored information
    rejected_prompt = f"""
    Analyze the following user input and identify any information that should be rejected or ignored for meal planning, along with clear reasons why.
    
    User Input: "{user_input}"
    Structured Data Used: {json.dumps(structured_data, indent=2)}
    
    Look for information that should be rejected or ignored such as:
    - Unsafe dietary practices or extreme restrictions
    - Contradictory information
    - Vague or unclear statements that couldn't be structured
    - Inappropriate food requests (e.g., unhealthy for stated conditions)
    - Information that doesn't relate to meal planning
    - Requests that conflict with health conditions
    
    Return JSON with:
    {{
        "rejected_items": [list of specific rejected information pieces],
        "reasons": [corresponding reasons for each rejection - same order as rejected_items]
    }}
    
    If no information was rejected, return empty arrays.
    """
    
    rejected_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=rejected_prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": RejectedInfo,
            "thinking_config": {"thinking_budget": 0}
        }
    )
    
    rejected_info = rejected_response.parsed.__dict__
    
    return structured_data, rejected_info

def generate_meal_plan(structured_data, full_input):
    prompt = f"""
    Create a one-day meal plan based on this structured data and user input.
    
    Structured Data: {json.dumps(structured_data, indent=2)}
    Full User Input: "{full_input}"
    
    Create a meal plan that:
    1. Respects all dietary restrictions and health conditions
    2. Considers cooking preference level
    3. Is balanced and realistic
    4. Uses simple, friendly language
    5. Includes brief explanations for key decisions
    
    Focus on practical, easy-to-follow meals.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": MealPlan,
            "thinking_config": {"thinking_budget": 0}
        }
    )
    
    return response.parsed.__dict__

@app.route('/reset', methods=['POST'])
def reset_conversation():
    session.clear()
    return jsonify({'status': 'reset'})

if __name__ == '__main__':
    app.run(debug=True)
