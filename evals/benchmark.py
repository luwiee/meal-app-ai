"""
Benchmark suite for the AI Meal Plan Assistant

This module provides standardized benchmarks for measuring AI performance
across different dimensions and comparing against baseline expectations.
"""

import time
import statistics
from typing import Dict, List, Any, Tuple
from datetime import datetime

from .evaluator import MealPlanEvaluator, EvalResult
from .test_cases import get_all_test_cases


class BenchmarkSuite:
    """Standardized benchmark suite for AI meal planning assistant"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.evaluator = MealPlanEvaluator(base_url)
        self.baseline_metrics = self._get_baseline_metrics()
    
    def _get_baseline_metrics(self) -> Dict[str, float]:
        """Define baseline performance expectations"""
        return {
            # Accuracy metrics (0.0 to 1.0)
            'data_extraction_accuracy': 0.85,
            'meal_plan_quality_score': 0.80,
            'safety_compliance_rate': 0.95,
            'conversation_flow_score': 0.75,
            
            # Performance metrics
            'average_response_time': 3.0,  # seconds
            'max_response_time': 8.0,      # seconds
            
            # User experience metrics
            'user_satisfaction_score': 0.80,
            'error_rate': 0.05,            # 5% error rate maximum
            
            # Overall system metrics
            'overall_pass_rate': 0.85,
            'overall_score': 0.80
        }
    
    def run_full_benchmark(self) -> Dict[str, Any]:
        """Run comprehensive benchmark suite"""
        print("🚀 Starting Full Benchmark Suite...")
        
        start_time = time.time()
        
        # Run all test cases
        test_cases = get_all_test_cases()
        suite = self.evaluator.run_evaluation_suite(test_cases)
        
        # Calculate benchmark metrics
        metrics = self._calculate_benchmark_metrics(suite.results)
        
        # Compare against baseline
        comparison = self._compare_against_baseline(metrics)
        
        # Generate benchmark report
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_execution_time': time.time() - start_time,
            'test_summary': {
                'total_tests': suite.total_tests,
                'passed_tests': suite.passed_tests,
                'failed_tests': suite.failed_tests,
                'pass_rate': suite.pass_rate,
                'average_score': suite.average_score
            },
            'benchmark_metrics': metrics,
            'baseline_comparison': comparison,
            'performance_grade': self._calculate_performance_grade(comparison),
            'recommendations': self._generate_recommendations(comparison)
        }
        
        return report
    
    def run_performance_benchmark(self) -> Dict[str, Any]:
        """Run focused performance benchmark"""
        print("⚡ Running Performance Benchmark...")
        
        performance_tests = [
            {
                'name': 'Simple Request',
                'message': 'I want to eat healthier.',
                'expected_max_time': 3.0
            },
            {
                'name': 'Complex Request',
                'message': 'I have diabetes, high blood pressure, and celiac disease. I need a meal plan that is low-carb, gluten-free, and heart-healthy.',
                'expected_max_time': 5.0
            },
            {
                'name': 'Multi-turn Conversation',
                'messages': [
                    'I want to lose weight.',
                    'I prefer vegetarian meals.',
                    'I have limited time for cooking.'
                ],
                'expected_max_time': 4.0
            }
        ]
        
        results = []
        
        for test in performance_tests:
            print(f"  Testing: {test['name']}")
            
            # Reset conversation
            self.evaluator._reset_conversation()
            
            start_time = time.time()
            
            try:
                if 'messages' in test:
                    # Multi-turn test
                    responses = []
                    for message in test['messages']:
                        response = self.evaluator._send_message(message)
                        responses.append(response)
                    final_response = responses[-1]
                else:
                    # Single message test
                    final_response = self.evaluator._send_message(test['message'])
                
                execution_time = time.time() - start_time
                
                results.append({
                    'test_name': test['name'],
                    'execution_time': execution_time,
                    'expected_max_time': test['expected_max_time'],
                    'within_threshold': execution_time <= test['expected_max_time'],
                    'response_received': final_response is not None,
                    'response_type': final_response.get('type', 'unknown') if final_response else 'none'
                })
                
            except Exception as e:
                results.append({
                    'test_name': test['name'],
                    'execution_time': -1,
                    'expected_max_time': test['expected_max_time'],
                    'within_threshold': False,
                    'response_received': False,
                    'error': str(e)
                })
        
        # Calculate performance metrics
        response_times = [r['execution_time'] for r in results if r['execution_time'] > 0]
        performance_metrics = {
            'average_response_time': statistics.mean(response_times) if response_times else 0,
            'max_response_time': max(response_times) if response_times else 0,
            'min_response_time': min(response_times) if response_times else 0,
            'tests_within_threshold': sum(1 for r in results if r['within_threshold']),
            'total_tests': len(results),
            'success_rate': sum(1 for r in results if r['response_received']) / len(results)
        }
        
        return {
            'timestamp': datetime.now().isoformat(),
            'performance_metrics': performance_metrics,
            'detailed_results': results,
            'baseline_comparison': {
                'average_response_time': {
                    'actual': performance_metrics['average_response_time'],
                    'baseline': self.baseline_metrics['average_response_time'],
                    'passes': performance_metrics['average_response_time'] <= self.baseline_metrics['average_response_time']
                },
                'max_response_time': {
                    'actual': performance_metrics['max_response_time'],
                    'baseline': self.baseline_metrics['max_response_time'],
                    'passes': performance_metrics['max_response_time'] <= self.baseline_metrics['max_response_time']
                }
            }
        }
    
    def run_accuracy_benchmark(self) -> Dict[str, Any]:
        """Run focused accuracy benchmark"""
        print("🎯 Running Accuracy Benchmark...")
        
        # Define accuracy test cases
        accuracy_tests = [
            {
                'input': 'I have diabetes and need low-carb meals.',
                'expected_conditions': ['diabetes'],
                'expected_restrictions': ['low-carb'],
                'category': 'health_condition_extraction'
            },
            {
                'input': 'I\'m vegetarian and allergic to nuts.',
                'expected_restrictions': ['vegetarian', 'nut-free'],
                'category': 'dietary_restriction_extraction'
            },
            {
                'input': 'I love chicken and vegetables but hate seafood.',
                'expected_likes': ['chicken', 'vegetables'],
                'expected_dislikes': ['seafood'],
                'category': 'preference_extraction'
            }
        ]
        
        results = []
        
        for test in accuracy_tests:
            print(f"  Testing: {test['category']}")
            
            # Reset conversation
            self.evaluator._reset_conversation()
            
            try:
                # Get meal plan response
                responses = []
                current_message = test['input']
                
                for _ in range(5):  # Max 5 interactions
                    response = self.evaluator._send_message(current_message)
                    responses.append(response)
                    
                    if response.get('type') == 'meal_plan':
                        break
                    elif response.get('type') == 'single_question':
                        current_message = "I'm flexible with that."
                    else:
                        current_message = "Please proceed with the meal plan."
                
                # Analyze accuracy
                final_response = responses[-1] if responses else {}
                structured_data = final_response.get('structured_data', {})
                
                accuracy_score = self._calculate_accuracy_score(test, structured_data)
                
                results.append({
                    'test_category': test['category'],
                    'accuracy_score': accuracy_score,
                    'expected_data': {k: v for k, v in test.items() if k.startswith('expected_')},
                    'actual_data': structured_data,
                    'passed': accuracy_score >= 0.8
                })
                
            except Exception as e:
                results.append({
                    'test_category': test['category'],
                    'accuracy_score': 0.0,
                    'error': str(e),
                    'passed': False
                })
        
        # Calculate overall accuracy metrics
        accuracy_scores = [r['accuracy_score'] for r in results]
        accuracy_metrics = {
            'average_accuracy': statistics.mean(accuracy_scores) if accuracy_scores else 0,
            'min_accuracy': min(accuracy_scores) if accuracy_scores else 0,
            'max_accuracy': max(accuracy_scores) if accuracy_scores else 0,
            'tests_passed': sum(1 for r in results if r['passed']),
            'total_tests': len(results),
            'pass_rate': sum(1 for r in results if r['passed']) / len(results) if results else 0
        }
        
        return {
            'timestamp': datetime.now().isoformat(),
            'accuracy_metrics': accuracy_metrics,
            'detailed_results': results,
            'baseline_comparison': {
                'data_extraction_accuracy': {
                    'actual': accuracy_metrics['average_accuracy'],
                    'baseline': self.baseline_metrics['data_extraction_accuracy'],
                    'passes': accuracy_metrics['average_accuracy'] >= self.baseline_metrics['data_extraction_accuracy']
                }
            }
        }
    
    def _calculate_benchmark_metrics(self, results: List[EvalResult]) -> Dict[str, float]:
        """Calculate comprehensive benchmark metrics from evaluation results"""
        if not results:
            return {}
        
        # Group results by category
        category_results = {}
        for result in results:
            category = result.test_case_id.split('_')[0]
            if category not in category_results:
                category_results[category] = []
            category_results[category].append(result)
        
        metrics = {}
        
        # Calculate category-specific metrics
        for category, cat_results in category_results.items():
            scores = [r.score for r in cat_results]
            pass_rate = sum(1 for r in cat_results if r.passed) / len(cat_results)
            
            if category == 'de':  # data extraction
                metrics['data_extraction_accuracy'] = statistics.mean(scores)
            elif category == 'mpq':  # meal plan quality
                metrics['meal_plan_quality_score'] = statistics.mean(scores)
            elif category == 'sc':  # safety compliance
                metrics['safety_compliance_rate'] = pass_rate
            elif category == 'cf':  # conversation flow
                metrics['conversation_flow_score'] = statistics.mean(scores)
        
        # Calculate performance metrics
        response_times = [r.execution_time for r in results]
        metrics['average_response_time'] = statistics.mean(response_times)
        metrics['max_response_time'] = max(response_times)
        
        # Calculate overall metrics
        all_scores = [r.score for r in results]
        metrics['overall_score'] = statistics.mean(all_scores)
        metrics['overall_pass_rate'] = sum(1 for r in results if r.passed) / len(results)
        
        # Calculate error rate
        error_count = sum(1 for r in results if r.errors)
        metrics['error_rate'] = error_count / len(results)
        
        # User experience score (composite)
        ux_factors = [
            metrics.get('average_response_time', 10) <= 3.0,  # Fast response
            metrics.get('error_rate', 1.0) <= 0.05,          # Low error rate
            metrics.get('conversation_flow_score', 0) >= 0.75 # Good conversation flow
        ]
        metrics['user_satisfaction_score'] = sum(ux_factors) / len(ux_factors)
        
        return metrics
    
    def _compare_against_baseline(self, metrics: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
        """Compare actual metrics against baseline expectations"""
        comparison = {}
        
        for metric_name, baseline_value in self.baseline_metrics.items():
            actual_value = metrics.get(metric_name, 0)
            
            if metric_name in ['average_response_time', 'max_response_time', 'error_rate']:
                # Lower is better for these metrics
                passes = actual_value <= baseline_value
                performance_ratio = baseline_value / actual_value if actual_value > 0 else 0
            else:
                # Higher is better for these metrics
                passes = actual_value >= baseline_value
                performance_ratio = actual_value / baseline_value if baseline_value > 0 else 0
            
            comparison[metric_name] = {
                'actual': actual_value,
                'baseline': baseline_value,
                'passes': passes,
                'performance_ratio': performance_ratio,
                'deviation': actual_value - baseline_value
            }
        
        return comparison
    
    def _calculate_performance_grade(self, comparison: Dict[str, Dict[str, Any]]) -> str:
        """Calculate overall performance grade"""
        passed_metrics = sum(1 for comp in comparison.values() if comp['passes'])
        total_metrics = len(comparison)
        pass_rate = passed_metrics / total_metrics if total_metrics > 0 else 0
        
        if pass_rate >= 0.95:
            return 'A+'
        elif pass_rate >= 0.90:
            return 'A'
        elif pass_rate >= 0.85:
            return 'B+'
        elif pass_rate >= 0.80:
            return 'B'
        elif pass_rate >= 0.75:
            return 'C+'
        elif pass_rate >= 0.70:
            return 'C'
        elif pass_rate >= 0.65:
            return 'D'
        else:
            return 'F'
    
    def _generate_recommendations(self, comparison: Dict[str, Dict[str, Any]]) -> List[str]:
        """Generate improvement recommendations based on benchmark results"""
        recommendations = []
        
        # Check each metric and provide specific recommendations
        for metric_name, comp in comparison.items():
            if not comp['passes']:
                if metric_name == 'data_extraction_accuracy':
                    recommendations.append(
                        "Improve data extraction accuracy by refining prompts and validation logic"
                    )
                elif metric_name == 'meal_plan_quality_score':
                    recommendations.append(
                        "Enhance meal plan quality by improving nutrition guidelines and meal variety"
                    )
                elif metric_name == 'safety_compliance_rate':
                    recommendations.append(
                        "Strengthen safety compliance by adding more comprehensive safety checks"
                    )
                elif metric_name == 'average_response_time':
                    recommendations.append(
                        f"Optimize response time - currently {comp['actual']:.1f}s vs target {comp['baseline']:.1f}s"
                    )
                elif metric_name == 'error_rate':
                    recommendations.append(
                        "Reduce error rate by improving error handling and input validation"
                    )
        
        if not recommendations:
            recommendations.append("Excellent performance! All metrics meet or exceed baseline expectations.")
        
        return recommendations
    
    def _calculate_accuracy_score(self, test: Dict[str, Any], structured_data: Dict[str, Any]) -> float:
        """Calculate accuracy score for a specific test"""
        score = 0.0
        total_checks = 0
        
        # Check expected conditions
        if 'expected_conditions' in test:
            expected = test['expected_conditions']
            actual = structured_data.get('health_conditions', [])
            overlap = len(set(expected) & set(actual))
            score += overlap / len(expected) if expected else 1.0
            total_checks += 1
        
        # Check expected restrictions
        if 'expected_restrictions' in test:
            expected = test['expected_restrictions']
            actual = structured_data.get('dietary_restrictions', [])
            overlap = len(set(expected) & set(actual))
            score += overlap / len(expected) if expected else 1.0
            total_checks += 1
        
        # Check expected likes
        if 'expected_likes' in test:
            expected = test['expected_likes']
            actual = structured_data.get('likes', [])
            overlap = len(set(expected) & set(actual))
            score += overlap / len(expected) if expected else 1.0
            total_checks += 1
        
        # Check expected dislikes
        if 'expected_dislikes' in test:
            expected = test['expected_dislikes']
            actual = structured_data.get('dislikes', [])
            overlap = len(set(expected) & set(actual))
            score += overlap / len(expected) if expected else 1.0
            total_checks += 1
        
        return score / total_checks if total_checks > 0 else 0.0
