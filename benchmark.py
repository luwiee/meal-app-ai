#!/usr/bin/env python3
"""
Benchmark Runner for AI Meal Plan Assistant

This script runs standardized benchmarks to measure AI performance
against baseline expectations and industry standards.

Usage:
    python benchmark.py [options]
    
Options:
    --suite SUITE          Benchmark suite to run: full, performance, accuracy (default: full)
    --base-url URL         Base URL for the application (default: http://localhost:5000)
    --output-dir DIR       Directory for output reports (default: benchmark_reports)
    --format FORMAT        Report format: json, csv, html (default: json)
    --verbose             Enable verbose output
    --help                Show this help message
"""

import argparse
import json
import sys
import time
from pathlib import Path
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from evals.benchmark import BenchmarkSuite


def main():
    parser = argparse.ArgumentParser(
        description="Run AI Meal Plan Assistant benchmarks",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--suite', 
        choices=['full', 'performance', 'accuracy'],
        default='full',
        help='Benchmark suite to run (default: full)'
    )
    
    parser.add_argument(
        '--base-url', 
        default='http://localhost:5000',
        help='Base URL for the application (default: http://localhost:5000)'
    )
    
    parser.add_argument(
        '--output-dir', 
        default='benchmark_reports',
        help='Directory for output reports (default: benchmark_reports)'
    )
    
    parser.add_argument(
        '--format', 
        choices=['json', 'csv', 'html'],
        default='json',
        help='Report format (default: json)'
    )
    
    parser.add_argument(
        '--verbose', 
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Initialize benchmark suite
    benchmark_suite = BenchmarkSuite(base_url=args.base_url)
    
    print(f"🏁 Starting AI Meal Plan Assistant Benchmark")
    print(f"📊 Suite: {args.suite}")
    print(f"🌐 Base URL: {args.base_url}")
    print(f"📁 Output Directory: {args.output_dir}")
    print("-" * 60)
    
    # Test connection
    try:
        import requests
        response = requests.get(args.base_url, timeout=5)
        if response.status_code != 200:
            print(f"⚠️  Warning: Application returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot connect to application: {e}")
        return 1
    
    # Run selected benchmark suite
    try:
        if args.suite == 'full':
            results = benchmark_suite.run_full_benchmark()
        elif args.suite == 'performance':
            results = benchmark_suite.run_performance_benchmark()
        elif args.suite == 'accuracy':
            results = benchmark_suite.run_accuracy_benchmark()
        
        # Generate timestamp for filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save results
        if args.format == 'json':
            filename = f"benchmark_{args.suite}_{timestamp}.json"
            filepath = output_dir / filename
            with open(filepath, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"📄 Results saved: {filepath}")
        
        # Display summary
        print(f"\n📊 Benchmark Results Summary:")
        print(f"⏱️  Execution Time: {results.get('total_execution_time', 0):.1f}s")
        
        if args.suite == 'full':
            grade = results.get('performance_grade', 'Unknown')
            print(f"🏆 Performance Grade: {grade}")
            
            if 'test_summary' in results:
                summary = results['test_summary']
                print(f"✅ Pass Rate: {summary.get('pass_rate', 0):.1%}")
                print(f"🎯 Average Score: {summary.get('average_score', 0):.2f}")
            
            if 'recommendations' in results:
                print(f"\n💡 Recommendations:")
                for rec in results['recommendations']:
                    print(f"   • {rec}")
        
        elif args.suite == 'performance':
            if 'performance_metrics' in results:
                metrics = results['performance_metrics']
                print(f"⚡ Average Response Time: {metrics.get('average_response_time', 0):.2f}s")
                print(f"🔥 Max Response Time: {metrics.get('max_response_time', 0):.2f}s")
                print(f"✅ Success Rate: {metrics.get('success_rate', 0):.1%}")
        
        elif args.suite == 'accuracy':
            if 'accuracy_metrics' in results:
                metrics = results['accuracy_metrics']
                print(f"🎯 Average Accuracy: {metrics.get('average_accuracy', 0):.2f}")
                print(f"📈 Pass Rate: {metrics.get('pass_rate', 0):.1%}")
        
        # Show baseline comparison if available
        if 'baseline_comparison' in results:
            print(f"\n📊 Baseline Comparison:")
            comparison = results['baseline_comparison']
            for metric, data in comparison.items():
                if isinstance(data, dict) and 'passes' in data:
                    status = "✅ PASS" if data['passes'] else "❌ FAIL"
                    print(f"   {metric}: {status} (Actual: {data.get('actual', 0):.2f}, Baseline: {data.get('baseline', 0):.2f})")
        
        # Determine exit code
        if args.suite == 'full':
            grade = results.get('performance_grade', 'F')
            if grade in ['A+', 'A', 'B+', 'B']:
                return 0
            else:
                return 1
        else:
            # For performance and accuracy suites, check if majority of metrics pass
            if 'baseline_comparison' in results:
                passed = sum(1 for data in results['baseline_comparison'].values() 
                           if isinstance(data, dict) and data.get('passes', False))
                total = len(results['baseline_comparison'])
                if passed / total >= 0.7:  # 70% pass rate
                    return 0
                else:
                    return 1
            return 0
    
    except Exception as e:
        print(f"❌ Benchmark failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
