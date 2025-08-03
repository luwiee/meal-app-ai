#!/usr/bin/env python3
"""
AI Meal Plan Assistant - Evaluation Runner

This script runs comprehensive evaluations of the AI meal planning assistant
and generates detailed reports on its performance across multiple dimensions.

Usage:
    python run_evals.py [options]
    
Options:
    --category CATEGORY     Run tests for specific category only
    --priority PRIORITY     Run tests with specific priority (critical, high, medium, low)
    --smoke                 Run smoke tests only (quick validation)
    --output-dir DIR        Directory for output reports (default: eval_reports)
    --base-url URL          Base URL for the application (default: http://localhost:5000)
    --format FORMAT         Report format: html, csv, json, all (default: html)
    --verbose              Enable verbose output
    --help                  Show this help message
"""

import argparse
import sys
import time
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from evals.evaluator import MealPlanEvaluator, EvalCategory
from evals.test_cases import (
    get_all_test_cases, 
    get_test_cases_by_category, 
    get_test_cases_by_priority,
    get_critical_test_cases,
    get_smoke_test_cases
)
from evals.reporter import EvaluationReporter


def main():
    parser = argparse.ArgumentParser(
        description="Run AI Meal Plan Assistant evaluations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_evals.py                           # Run all tests
    python run_evals.py --smoke                   # Run smoke tests only
    python run_evals.py --category safety_compliance  # Run safety tests only
    python run_evals.py --priority critical       # Run critical tests only
    python run_evals.py --format all              # Generate all report formats
        """
    )
    
    parser.add_argument(
        '--category', 
        choices=[cat.value for cat in EvalCategory],
        help='Run tests for specific category only'
    )
    
    parser.add_argument(
        '--priority', 
        choices=['critical', 'high', 'medium', 'low'],
        help='Run tests with specific priority level'
    )
    
    parser.add_argument(
        '--smoke', 
        action='store_true',
        help='Run smoke tests only (quick validation)'
    )
    
    parser.add_argument(
        '--output-dir', 
        default='eval_reports',
        help='Directory for output reports (default: eval_reports)'
    )
    
    parser.add_argument(
        '--base-url', 
        default='http://localhost:5000',
        help='Base URL for the application (default: http://localhost:5000)'
    )
    
    parser.add_argument(
        '--format', 
        choices=['html', 'csv', 'json', 'all'],
        default='html',
        help='Report format (default: html)'
    )
    
    parser.add_argument(
        '--verbose', 
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Initialize evaluator and reporter
    evaluator = MealPlanEvaluator(base_url=args.base_url)
    reporter = EvaluationReporter(output_dir=args.output_dir)
    
    # Select test cases based on arguments
    if args.smoke:
        test_cases = get_smoke_test_cases()
        test_description = "Smoke Tests"
    elif args.category:
        category = EvalCategory(args.category)
        test_cases = get_test_cases_by_category(category)
        test_description = f"{args.category.replace('_', ' ').title()} Tests"
    elif args.priority:
        test_cases = get_test_cases_by_priority(args.priority)
        test_description = f"{args.priority.title()} Priority Tests"
    else:
        test_cases = get_all_test_cases()
        test_description = "All Tests"
    
    if not test_cases:
        print("❌ No test cases found matching the specified criteria.")
        return 1
    
    print(f"🚀 Starting AI Meal Plan Assistant Evaluation")
    print(f"📋 Test Suite: {test_description}")
    print(f"🔢 Total Tests: {len(test_cases)}")
    print(f"🌐 Base URL: {args.base_url}")
    print(f"📁 Output Directory: {args.output_dir}")
    print(f"📊 Report Format: {args.format}")
    print("-" * 60)
    
    # Test connection to the application
    try:
        import requests
        response = requests.get(args.base_url, timeout=5)
        if response.status_code != 200:
            print(f"⚠️  Warning: Application at {args.base_url} returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot connect to application at {args.base_url}: {e}")
        print("   Please ensure the application is running before starting evaluations.")
        return 1
    
    # Run evaluations
    start_time = time.time()
    
    try:
        suite = evaluator.run_evaluation_suite(test_cases)
        
        total_time = time.time() - start_time
        
        # Print summary
        print(f"\n📊 Evaluation Complete!")
        print(f"⏱️  Total Time: {total_time:.1f}s")
        print(f"✅ Passed: {suite.passed_tests}/{suite.total_tests} ({suite.pass_rate:.1%})")
        print(f"❌ Failed: {suite.failed_tests}")
        print(f"🎯 Average Score: {suite.average_score:.2f}")
        
        # Show failed tests if any
        failed_tests = [r for r in suite.results if not r.passed]
        if failed_tests:
            print(f"\n❌ Failed Tests ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"   - {test.test_case_id}: Score {test.score:.2f}")
                if test.errors and args.verbose:
                    for error in test.errors[:2]:  # Show first 2 errors
                        print(f"     Error: {error}")
        
        # Generate reports
        print(f"\n📄 Generating Reports...")
        
        report_files = []
        
        if args.format in ['html', 'all']:
            html_file = reporter.generate_html_report(suite)
            report_files.append(html_file)
            print(f"📝 HTML Report: {html_file}")
        
        if args.format in ['csv', 'all']:
            csv_file = reporter.generate_csv_report(suite)
            report_files.append(csv_file)
            print(f"📊 CSV Report: {csv_file}")
        
        if args.format in ['json', 'all']:
            json_file = reporter.generate_json_report(suite)
            report_files.append(json_file)
            print(f"📋 JSON Report: {json_file}")
        
        # Generate summary to console
        if args.verbose:
            print(f"\n📋 Summary Report:")
            print(reporter.generate_summary_report(suite))
        
        # Return exit code based on pass rate
        if suite.pass_rate >= 0.9:
            print(f"\n🎉 Excellent! All systems performing well.")
            return 0
        elif suite.pass_rate >= 0.8:
            print(f"\n👍 Good performance with room for improvement.")
            return 0
        elif suite.pass_rate >= 0.7:
            print(f"\n⚠️  Acceptable performance but needs attention.")
            return 1
        else:
            print(f"\n🚨 Poor performance - immediate attention required.")
            return 1
            
    except KeyboardInterrupt:
        print(f"\n🛑 Evaluation interrupted by user.")
        return 130
    except Exception as e:
        print(f"\n❌ Evaluation failed with error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
