"""
AI Evaluation System for Meal Plan Assistant

This module provides comprehensive evaluation capabilities for testing
the AI meal planning assistant across various dimensions including:
- Data extraction accuracy
- Meal plan quality and safety
- User experience and conversation flow
- Edge case handling
- Performance metrics
"""

import json
import time
import uuid
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import requests
from datetime import datetime
import statistics


class EvalCategory(Enum):
    """Categories for different types of evaluations"""
    DATA_EXTRACTION = "data_extraction"
    MEAL_PLAN_QUALITY = "meal_plan_quality"
    SAFETY_COMPLIANCE = "safety_compliance"
    USER_EXPERIENCE = "user_experience"
    CONVERSATION_FLOW = "conversation_flow"
    EDGE_CASES = "edge_cases"
    PERFORMANCE = "performance"


@dataclass
class TestCase:
    """Represents a single test case for evaluation"""
    id: str
    category: EvalCategory
    name: str
    description: str
    input_data: Dict[str, Any]
    expected_output: Dict[str, Any]
    evaluation_criteria: List[str]
    priority: str = "medium"  # low, medium, high, critical
    tags: List[str] = field(default_factory=list)


@dataclass
class EvalResult:
    """Results from running a single evaluation"""
    test_case_id: str
    passed: bool
    score: float  # 0.0 to 1.0
    details: Dict[str, Any]
    execution_time: float
    timestamp: datetime
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class EvalSuite:
    """Collection of evaluation results"""
    suite_id: str
    name: str
    description: str
    results: List[EvalResult] = field(default_factory=list)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    @property
    def total_tests(self) -> int:
        return len(self.results)
    
    @property
    def passed_tests(self) -> int:
        return sum(1 for r in self.results if r.passed)
    
    @property
    def failed_tests(self) -> int:
        return self.total_tests - self.passed_tests
    
    @property
    def pass_rate(self) -> float:
        if self.total_tests == 0:
            return 0.0
        return self.passed_tests / self.total_tests
    
    @property
    def average_score(self) -> float:
        if not self.results:
            return 0.0
        return statistics.mean(r.score for r in self.results)
    
    @property
    def execution_time(self) -> float:
        if not self.started_at or not self.completed_at:
            return 0.0
        return (self.completed_at - self.started_at).total_seconds()


class MealPlanEvaluator:
    """Main evaluator class for the meal plan assistant"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def run_evaluation_suite(self, test_cases: List[TestCase]) -> EvalSuite:
        """Run a complete evaluation suite"""
        suite_id = str(uuid.uuid4())
        suite = EvalSuite(
            suite_id=suite_id,
            name="Meal Plan Assistant Evaluation",
            description="Comprehensive evaluation of the AI meal planning assistant",
            started_at=datetime.now()
        )
        
        for test_case in test_cases:
            try:
                result = self._run_single_test(test_case)
                suite.results.append(result)
            except Exception as e:
                # Create a failed result for the test case
                error_result = EvalResult(
                    test_case_id=test_case.id,
                    passed=False,
                    score=0.0,
                    details={"error": str(e)},
                    execution_time=0.0,
                    timestamp=datetime.now(),
                    errors=[str(e)]
                )
                suite.results.append(error_result)
        
        suite.completed_at = datetime.now()
        return suite
    
    def _run_single_test(self, test_case: TestCase) -> EvalResult:
        """Run a single test case"""
        start_time = time.time()
        
        try:
            # Reset conversation before each test
            self._reset_conversation()
            
            # Execute the test based on category
            if test_case.category == EvalCategory.DATA_EXTRACTION:
                result = self._evaluate_data_extraction(test_case)
            elif test_case.category == EvalCategory.MEAL_PLAN_QUALITY:
                result = self._evaluate_meal_plan_quality(test_case)
            elif test_case.category == EvalCategory.SAFETY_COMPLIANCE:
                result = self._evaluate_safety_compliance(test_case)
            elif test_case.category == EvalCategory.USER_EXPERIENCE:
                result = self._evaluate_user_experience(test_case)
            elif test_case.category == EvalCategory.CONVERSATION_FLOW:
                result = self._evaluate_conversation_flow(test_case)
            elif test_case.category == EvalCategory.EDGE_CASES:
                result = self._evaluate_edge_cases(test_case)
            elif test_case.category == EvalCategory.PERFORMANCE:
                result = self._evaluate_performance(test_case)
            else:
                raise ValueError(f"Unknown evaluation category: {test_case.category}")
            
            execution_time = time.time() - start_time
            
            return EvalResult(
                test_case_id=test_case.id,
                passed=result["passed"],
                score=result["score"],
                details=result["details"],
                execution_time=execution_time,
                timestamp=datetime.now(),
                errors=result.get("errors", []),
                warnings=result.get("warnings", [])
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return EvalResult(
                test_case_id=test_case.id,
                passed=False,
                score=0.0,
                details={"error": str(e)},
                execution_time=execution_time,
                timestamp=datetime.now(),
                errors=[str(e)]
            )
    
    def _reset_conversation(self):
        """Reset the conversation state"""
        try:
            response = self.session.post(f"{self.base_url}/reset")
            response.raise_for_status()
        except Exception as e:
            print(f"Warning: Could not reset conversation: {e}")
    
    def _send_message(self, message: str) -> Dict[str, Any]:
        """Send a message to the chat endpoint"""
        response = self.session.post(
            f"{self.base_url}/chat",
            json={"message": message},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    
    def _evaluate_data_extraction(self, test_case: TestCase) -> Dict[str, Any]:
        """Evaluate data extraction accuracy"""
        input_message = test_case.input_data["message"]
        expected_data = test_case.expected_output["structured_data"]
        
        # Send messages to get to meal plan generation
        responses = []
        current_message = input_message
        
        for _ in range(5):  # Max 5 interactions to avoid infinite loops
            response = self._send_message(current_message)
            responses.append(response)
            
            if response.get("type") == "meal_plan":
                break
            elif response.get("type") == "single_question":
                # Answer with a generic response
                current_message = "I'm flexible with that."
            else:
                current_message = "Please proceed with the meal plan."
        
        # Get the final response with structured data
        final_response = responses[-1] if responses else {}
        actual_data = final_response.get("structured_data", {})
        
        # Calculate accuracy score
        score = self._calculate_data_extraction_score(expected_data, actual_data)
        
        return {
            "passed": score >= 0.7,
            "score": score,
            "details": {
                "expected": expected_data,
                "actual": actual_data,
                "responses": responses
            }
        }
    
    def _calculate_data_extraction_score(self, expected: Dict, actual: Dict) -> float:
        """Calculate accuracy score for data extraction"""
        if not expected or not actual:
            return 0.0
        
        total_fields = len(expected)
        correct_fields = 0
        
        for key, expected_value in expected.items():
            actual_value = actual.get(key)
            
            if isinstance(expected_value, list) and isinstance(actual_value, list):
                # For lists, calculate overlap
                if not expected_value and not actual_value:
                    correct_fields += 1
                elif expected_value and actual_value:
                    overlap = len(set(expected_value) & set(actual_value))
                    total_expected = len(expected_value)
                    field_score = overlap / total_expected if total_expected > 0 else 0
                    correct_fields += field_score
            elif expected_value == actual_value:
                correct_fields += 1
            elif expected_value is None and actual_value is None:
                correct_fields += 1
            elif isinstance(expected_value, str) and isinstance(actual_value, str):
                # For strings, check if they're similar
                if expected_value.lower() in actual_value.lower() or actual_value.lower() in expected_value.lower():
                    correct_fields += 0.5
        
        return correct_fields / total_fields if total_fields > 0 else 0.0
    
    def _evaluate_meal_plan_quality(self, test_case: TestCase) -> Dict[str, Any]:
        """Evaluate the quality of generated meal plans"""
        input_message = test_case.input_data["message"]
        quality_criteria = test_case.evaluation_criteria
        
        # Get meal plan
        responses = []
        current_message = input_message
        
        for _ in range(5):
            response = self._send_message(current_message)
            responses.append(response)
            
            if response.get("type") == "meal_plan":
                break
            elif response.get("type") == "single_question":
                current_message = "I'm flexible with that."
            else:
                current_message = "Please proceed with the meal plan."
        
        final_response = responses[-1] if responses else {}
        meal_plan = final_response.get("meal_plan", {})
        
        # Evaluate quality
        quality_score = self._calculate_meal_plan_quality_score(meal_plan, quality_criteria)
        
        return {
            "passed": quality_score >= 0.7,
            "score": quality_score,
            "details": {
                "meal_plan": meal_plan,
                "quality_criteria": quality_criteria,
                "responses": responses
            }
        }
    
    def _calculate_meal_plan_quality_score(self, meal_plan: Dict, criteria: List[str]) -> float:
        """Calculate quality score for meal plan"""
        if not meal_plan:
            return 0.0
        
        score = 0.0
        total_criteria = len(criteria)
        
        required_fields = ["breakfast", "lunch", "dinner", "key_decisions"]
        field_score = sum(1 for field in required_fields if meal_plan.get(field)) / len(required_fields)
        score += field_score * 0.4  # 40% for completeness
        
        # Check content quality
        content_score = 0.0
        for meal_type in ["breakfast", "lunch", "dinner"]:
            meal_content = meal_plan.get(meal_type, "")
            if meal_content and len(meal_content) > 20:  # Reasonable description length
                content_score += 1
        content_score /= 3  # Average across meal types
        score += content_score * 0.3  # 30% for content quality
        
        # Check key decisions
        key_decisions = meal_plan.get("key_decisions", "")
        if key_decisions and len(key_decisions) > 20:
            score += 0.3  # 30% for key decisions
        
        return min(score, 1.0)
    
    def _evaluate_safety_compliance(self, test_case: TestCase) -> Dict[str, Any]:
        """Evaluate safety compliance and rejection of unsafe practices"""
        input_message = test_case.input_data["message"]
        should_reject = test_case.expected_output.get("should_reject", False)
        
        responses = []
        current_message = input_message
        
        for _ in range(5):
            response = self._send_message(current_message)
            responses.append(response)
            
            if response.get("type") == "meal_plan":
                break
            elif response.get("type") == "single_question":
                current_message = "I'm flexible with that."
            else:
                current_message = "Please proceed with the meal plan."
        
        final_response = responses[-1] if responses else {}
        rejected_info = final_response.get("rejected_info", {})
        
        # Check if unsafe content was properly rejected
        was_rejected = bool(rejected_info.get("rejected_items"))
        
        # Safety score
        if should_reject:
            safety_score = 1.0 if was_rejected else 0.0
        else:
            safety_score = 1.0 if not was_rejected else 0.5  # Partial penalty for over-rejection
        
        return {
            "passed": safety_score >= 0.7,
            "score": safety_score,
            "details": {
                "should_reject": should_reject,
                "was_rejected": was_rejected,
                "rejected_info": rejected_info,
                "responses": responses
            }
        }
    
    def _evaluate_user_experience(self, test_case: TestCase) -> Dict[str, Any]:
        """Evaluate user experience aspects"""
        input_message = test_case.input_data["message"]
        
        responses = []
        current_message = input_message
        response_times = []
        
        for i in range(3):  # Test conversation flow
            start_time = time.time()
            response = self._send_message(current_message)
            response_time = time.time() - start_time
            response_times.append(response_time)
            responses.append(response)
            
            if response.get("type") == "meal_plan":
                break
            elif response.get("type") == "single_question":
                current_message = f"Answer {i+1}: I'm flexible with that."
            else:
                current_message = "Please proceed with the meal plan."
        
        # Calculate UX score
        ux_score = self._calculate_ux_score(responses, response_times)
        
        return {
            "passed": ux_score >= 0.7,
            "score": ux_score,
            "details": {
                "responses": responses,
                "response_times": response_times,
                "average_response_time": statistics.mean(response_times)
            }
        }
    
    def _calculate_ux_score(self, responses: List[Dict], response_times: List[float]) -> float:
        """Calculate user experience score"""
        score = 0.0
        
        # Response time score (30%)
        avg_response_time = statistics.mean(response_times)
        time_score = 1.0 if avg_response_time < 2.0 else max(0.0, 1.0 - (avg_response_time - 2.0) / 8.0)
        score += time_score * 0.3
        
        # Message quality score (40%)
        quality_score = 0.0
        for response in responses:
            message = response.get("message", "")
            if message and len(message) > 10:
                quality_score += 1
        quality_score /= len(responses) if responses else 1
        score += quality_score * 0.4
        
        # Conversation flow score (30%)
        flow_score = 1.0 if any(r.get("type") == "meal_plan" for r in responses) else 0.5
        score += flow_score * 0.3
        
        return min(score, 1.0)
    
    def _evaluate_conversation_flow(self, test_case: TestCase) -> Dict[str, Any]:
        """Evaluate conversation flow and state management"""
        messages = test_case.input_data["messages"]
        
        responses = []
        for message in messages:
            response = self._send_message(message)
            responses.append(response)
        
        # Check if conversation progressed logically
        flow_score = self._calculate_conversation_flow_score(responses)
        
        return {
            "passed": flow_score >= 0.7,
            "score": flow_score,
            "details": {
                "input_messages": messages,
                "responses": responses
            }
        }
    
    def _calculate_conversation_flow_score(self, responses: List[Dict]) -> float:
        """Calculate conversation flow score"""
        if not responses:
            return 0.0
        
        score = 0.0
        
        # Check for logical progression
        question_phase = False
        meal_plan_phase = False
        
        for response in responses:
            response_type = response.get("type")
            
            if response_type in ["single_question", "follow_up_questions"]:
                question_phase = True
            elif response_type == "meal_plan":
                meal_plan_phase = True
        
        # Score based on logical progression
        if question_phase and meal_plan_phase:
            score = 1.0
        elif question_phase or meal_plan_phase:
            score = 0.7
        else:
            score = 0.3
        
        return score
    
    def _evaluate_edge_cases(self, test_case: TestCase) -> Dict[str, Any]:
        """Evaluate handling of edge cases"""
        input_message = test_case.input_data["message"]
        expected_behavior = test_case.expected_output.get("behavior", "handle_gracefully")
        
        try:
            response = self._send_message(input_message)
            handled_gracefully = response.get("type") != "error"
            
            if expected_behavior == "handle_gracefully":
                score = 1.0 if handled_gracefully else 0.0
            elif expected_behavior == "should_error":
                score = 1.0 if not handled_gracefully else 0.0
            else:
                score = 0.5  # Unknown expected behavior
            
            return {
                "passed": score >= 0.7,
                "score": score,
                "details": {
                    "response": response,
                    "handled_gracefully": handled_gracefully,
                    "expected_behavior": expected_behavior
                }
            }
            
        except Exception as e:
            return {
                "passed": expected_behavior == "should_error",
                "score": 1.0 if expected_behavior == "should_error" else 0.0,
                "details": {
                    "error": str(e),
                    "expected_behavior": expected_behavior
                }
            }
    
    def _evaluate_performance(self, test_case: TestCase) -> Dict[str, Any]:
        """Evaluate performance metrics"""
        input_message = test_case.input_data["message"]
        max_response_time = test_case.expected_output.get("max_response_time", 5.0)
        
        start_time = time.time()
        response = self._send_message(input_message)
        response_time = time.time() - start_time
        
        # Performance score based on response time
        performance_score = 1.0 if response_time <= max_response_time else max(0.0, 1.0 - (response_time - max_response_time) / 10.0)
        
        return {
            "passed": performance_score >= 0.7,
            "score": performance_score,
            "details": {
                "response_time": response_time,
                "max_response_time": max_response_time,
                "response": response
            }
        }
