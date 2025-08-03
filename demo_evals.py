#!/usr/bin/env python3
"""
Demo script for AI Meal Plan Assistant Evaluation System

This script demonstrates the key features of the evaluation system
with a guided walkthrough of different evaluation types.
"""

import sys
import time
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from evals.evaluator import MealPlanEvaluator
from evals.test_cases import (
    get_smoke_test_cases,
    get_test_cases_by_category,
    get_critical_test_cases,
    EvalCategory
)
from evals.reporter import EvaluationReporter
from evals.benchmark import BenchmarkSuite


def print_banner():
    """Print a welcome banner"""
    print("=" * 80)
    print("🤖 AI Meal Plan Assistant - Evaluation System Demo")
    print("=" * 80)
    print()


def print_section(title):
    """Print a section header"""
    print(f"\n{'='*20} {title} {'='*20}")
    print()


def demo_smoke_tests():
    """Demonstrate smoke testing"""
    print_section("🚀 Smoke Tests Demo")
    print("Smoke tests provide quick validation of core functionality.")
    print("These tests run fast and catch major issues early.")
    print()
    
    evaluator = MealPlanEvaluator()
    test_cases = get_smoke_test_cases()
    
    print(f"Running {len(test_cases)} smoke tests...")
    print()
    
    try:
        suite = evaluator.run_evaluation_suite(test_cases)
        
        print(f"✅ Smoke Tests Complete!")
        print(f"📊 Results: {suite.passed_tests}/{suite.total_tests} passed ({suite.pass_rate:.1%})")
        print(f"🎯 Average Score: {suite.average_score:.2f}")
        print(f"⏱️  Execution Time: {suite.execution_time:.1f}s")
        
        if suite.pass_rate >= 0.8:
            print("🎉 Smoke tests PASSED - System is healthy!")
        else:
            print("⚠️  Smoke tests FAILED - System needs attention")
            
    except Exception as e:
        print(f"❌ Smoke tests failed to run: {e}")
        print("   Make sure the Flask app is running on localhost:5000")


def demo_category_testing():
    """Demonstrate category-specific testing"""
    print_section("📋 Category-Specific Testing Demo")
    print("Testing specific aspects of the AI system in detail.")
    print()
    
    # Test safety compliance
    print("🔒 Testing Safety Compliance...")
    evaluator = MealPlanEvaluator()
    safety_tests = get_test_cases_by_category(EvalCategory.SAFETY_COMPLIANCE)
    
    try:
        suite = evaluator.run_evaluation_suite(safety_tests)
        
        print(f"   Results: {suite.passed_tests}/{suite.total_tests} passed")
        print(f"   Safety compliance is {'GOOD' if suite.pass_rate >= 0.9 else 'NEEDS IMPROVEMENT'}")
        
    except Exception as e:
        print(f"   ❌ Safety tests failed: {e}")


def demo_performance_benchmarking():
    """Demonstrate performance benchmarking"""
    print_section("⚡ Performance Benchmarking Demo")
    print("Measuring AI performance against standardized benchmarks.")
    print()
    
    try:
        benchmark_suite = BenchmarkSuite()
        
        print("Running performance benchmark...")
        results = benchmark_suite.run_performance_benchmark()
        
        metrics = results.get('performance_metrics', {})
        print(f"📊 Performance Results:")
        print(f"   Average Response Time: {metrics.get('average_response_time', 0):.2f}s")
        print(f"   Max Response Time: {metrics.get('max_response_time', 0):.2f}s")
        print(f"   Success Rate: {metrics.get('success_rate', 0):.1%}")
        
        # Check against baselines
        baseline_comparison = results.get('baseline_comparison', {})
        avg_time_data = baseline_comparison.get('average_response_time', {})
        
        if avg_time_data.get('passes', False):
            print("   ✅ Performance meets baseline expectations")
        else:
            print("   ⚠️  Performance below baseline expectations")
            
    except Exception as e:
        print(f"❌ Performance benchmark failed: {e}")


def demo_report_generation():
    """Demonstrate report generation"""
    print_section("📊 Report Generation Demo")
    print("Generating comprehensive evaluation reports.")
    print()
    
    try:
        evaluator = MealPlanEvaluator()
        reporter = EvaluationReporter(output_dir="demo_reports")
        
        # Run a small set of tests for demo
        test_cases = get_critical_test_cases()[:3]  # Just first 3 critical tests
        
        print(f"Running {len(test_cases)} tests for report generation...")
        suite = evaluator.run_evaluation_suite(test_cases)
        
        # Generate different report formats
        print("Generating reports...")
        
        html_report = reporter.generate_html_report(suite, "demo_report.html")
        csv_report = reporter.generate_csv_report(suite, "demo_report.csv")
        json_report = reporter.generate_json_report(suite, "demo_report.json")
        
        print(f"📄 Generated Reports:")
        print(f"   HTML: {html_report}")
        print(f"   CSV:  {csv_report}")
        print(f"   JSON: {json_report}")
        
        # Show summary
        summary = reporter.generate_summary_report(suite)
        print(f"\n📋 Summary Report:")
        print(summary)
        
    except Exception as e:
        print(f"❌ Report generation failed: {e}")


def demo_evaluation_insights():
    """Show insights from evaluation results"""
    print_section("💡 Evaluation Insights Demo")
    print("Key insights from AI evaluation system:")
    print()
    
    insights = [
        "🎯 Data Extraction: Tests how well the AI extracts structured information",
        "🍽️  Meal Plan Quality: Evaluates nutritional appropriateness and variety", 
        "🔒 Safety Compliance: Validates rejection of unsafe dietary practices",
        "⚡ Performance: Measures response times and system reliability",
        "🗣️  User Experience: Tests conversational flow and user satisfaction",
        "🔄 Edge Cases: Validates handling of unusual or problematic inputs",
        "📈 Benchmarking: Compares performance against industry standards"
    ]
    
    for insight in insights:
        print(f"   {insight}")
        time.sleep(0.5)  # Dramatic pause for demo
    
    print()
    print("🚀 This comprehensive evaluation system ensures:")
    print("   • Consistent AI performance")
    print("   • User safety and satisfaction")
    print("   • Reliable system operation")
    print("   • Continuous improvement tracking")


def main():
    """Main demo function"""
    print_banner()
    
    print("This demo showcases the AI Evaluation System features.")
    print("Make sure the Flask app is running on localhost:5000 before continuing.")
    print()
    
    input("Press Enter to start the demo...")
    
    # Test connection
    try:
        import requests
        response = requests.get("http://localhost:5000", timeout=5)
        if response.status_code == 200:
            print("✅ Flask app is running - starting demo")
        else:
            print(f"⚠️  Flask app returned status {response.status_code} - continuing anyway")
    except Exception as e:
        print(f"❌ Cannot connect to Flask app: {e}")
        print("   Demo will continue but tests may fail")
    
    # Run demo sections
    try:
        demo_smoke_tests()
        input("\nPress Enter for next demo...")
        
        demo_category_testing()
        input("\nPress Enter for next demo...")
        
        demo_performance_benchmarking()
        input("\nPress Enter for next demo...")
        
        demo_report_generation()
        input("\nPress Enter for final insights...")
        
        demo_evaluation_insights()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Demo interrupted by user")
        return
    except Exception as e:
        print(f"\n❌ Demo encountered an error: {e}")
        return
    
    print("\n" + "="*80)
    print("🎉 Demo Complete!")
    print("="*80)
    print()
    print("Next steps:")
    print("1. Run full evaluations: python run_evals.py")
    print("2. Run benchmarks: python benchmark.py")
    print("3. Check generated reports in demo_reports/ folder")
    print("4. Set up CI/CD with the included GitHub Actions workflow")
    print()
    print("For more information, see evals/README.md")


if __name__ == "__main__":
    main()
