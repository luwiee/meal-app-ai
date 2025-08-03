"""
Reporting and visualization utilities for AI evaluation results

This module provides comprehensive reporting capabilities including:
- HTML report generation
- CSV export functionality
- Performance metrics analysis
- Visualization of evaluation results
"""

import json
import csv
import html
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path
import statistics

from .evaluator import EvalSuite, EvalResult, EvalCategory


class EvaluationReporter:
    """Handles generation of evaluation reports in various formats"""
    
    def __init__(self, output_dir: str = "eval_reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_html_report(self, suite: EvalSuite, filename: str = None) -> str:
        """Generate comprehensive HTML report"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"eval_report_{timestamp}.html"
        
        filepath = self.output_dir / filename
        
        html_content = self._generate_html_content(suite)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(filepath)
    
    def generate_csv_report(self, suite: EvalSuite, filename: str = None) -> str:
        """Generate CSV report with detailed results"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"eval_results_{timestamp}.csv"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'Test ID', 'Category', 'Name', 'Passed', 'Score', 'Execution Time (s)',
                'Timestamp', 'Errors', 'Warnings', 'Details'
            ])
            
            # Results
            for result in suite.results:
                writer.writerow([
                    result.test_case_id,
                    result.test_case_id.split('_')[0],  # Extract category from ID
                    result.details.get('name', 'Unknown'),
                    result.passed,
                    f"{result.score:.3f}",
                    f"{result.execution_time:.3f}",
                    result.timestamp.isoformat(),
                    '; '.join(result.errors) if result.errors else '',
                    '; '.join(result.warnings) if result.warnings else '',
                    json.dumps(result.details, default=str)
                ])
        
        return str(filepath)
    
    def generate_json_report(self, suite: EvalSuite, filename: str = None) -> str:
        """Generate JSON report with full details"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"eval_results_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        # Convert suite to serializable format
        suite_dict = {
            'suite_id': suite.suite_id,
            'name': suite.name,
            'description': suite.description,
            'started_at': suite.started_at.isoformat() if suite.started_at else None,
            'completed_at': suite.completed_at.isoformat() if suite.completed_at else None,
            'total_tests': suite.total_tests,
            'passed_tests': suite.passed_tests,
            'failed_tests': suite.failed_tests,
            'pass_rate': suite.pass_rate,
            'average_score': suite.average_score,
            'execution_time': suite.execution_time,
            'results': []
        }
        
        for result in suite.results:
            result_dict = {
                'test_case_id': result.test_case_id,
                'passed': result.passed,
                'score': result.score,
                'execution_time': result.execution_time,
                'timestamp': result.timestamp.isoformat(),
                'errors': result.errors,
                'warnings': result.warnings,
                'details': result.details
            }
            suite_dict['results'].append(result_dict)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(suite_dict, f, indent=2, default=str)
        
        return str(filepath)
    
    def _generate_html_content(self, suite: EvalSuite) -> str:
        """Generate HTML content for the evaluation report"""
        
        # Calculate category statistics
        category_stats = self._calculate_category_stats(suite.results)
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Meal Plan Assistant - Evaluation Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .summary-card h3 {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .summary-card .value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #4CAF50;
        }}
        
        .summary-card .value.failed {{
            color: #f44336;
        }}
        
        .summary-card .value.warning {{
            color: #ff9800;
        }}
        
        .category-stats {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        
        .category-stats h2 {{
            margin-bottom: 20px;
            color: #333;
        }}
        
        .category-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }}
        
        .category-item {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
        }}
        
        .category-item.failed {{
            border-left-color: #f44336;
        }}
        
        .category-item.warning {{
            border-left-color: #ff9800;
        }}
        
        .category-name {{
            font-weight: bold;
            margin-bottom: 5px;
            text-transform: capitalize;
        }}
        
        .category-metrics {{
            display: flex;
            justify-content: space-between;
            font-size: 0.9em;
            color: #666;
        }}
        
        .detailed-results {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .detailed-results h2 {{
            margin-bottom: 20px;
            color: #333;
        }}
        
        .test-result {{
            border: 1px solid #ddd;
            border-radius: 8px;
            margin-bottom: 15px;
            overflow: hidden;
        }}
        
        .test-result.passed {{
            border-left: 4px solid #4CAF50;
        }}
        
        .test-result.failed {{
            border-left: 4px solid #f44336;
        }}
        
        .test-header {{
            background: #f8f9fa;
            padding: 15px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .test-header:hover {{
            background: #e9ecef;
        }}
        
        .test-info {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        .test-status {{
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }}
        
        .test-status.passed {{
            background: #d4edda;
            color: #155724;
        }}
        
        .test-status.failed {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .test-details {{
            padding: 15px;
            display: none;
            border-top: 1px solid #ddd;
        }}
        
        .test-details.expanded {{
            display: block;
        }}
        
        .test-score {{
            font-size: 1.2em;
            font-weight: bold;
            color: #4CAF50;
        }}
        
        .test-score.failed {{
            color: #f44336;
        }}
        
        .test-execution-time {{
            font-size: 0.9em;
            color: #666;
        }}
        
        .collapsible-section {{
            margin-top: 15px;
        }}
        
        .collapsible-header {{
            background: #f8f9fa;
            padding: 10px;
            cursor: pointer;
            border-radius: 5px;
            font-weight: bold;
        }}
        
        .collapsible-content {{
            display: none;
            padding: 10px;
            background: #fff;
            border: 1px solid #ddd;
            border-radius: 0 0 5px 5px;
        }}
        
        .collapsible-content.expanded {{
            display: block;
        }}
        
        .json-display {{
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            font-family: monospace;
            font-size: 0.85em;
            overflow-x: auto;
            white-space: pre-wrap;
        }}
        
        .error-list {{
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 5px;
            padding: 10px;
            margin-top: 10px;
        }}
        
        .warning-list {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 10px;
            margin-top: 10px;
        }}
        
        .timestamp {{
            font-size: 0.8em;
            color: #999;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}
            
            .summary {{
                grid-template-columns: 1fr;
            }}
            
            .category-grid {{
                grid-template-columns: 1fr;
            }}
            
            .test-info {{
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Meal Plan Assistant</h1>
            <p>Evaluation Report - {suite.name}</p>
            <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <h3>Total Tests</h3>
                <div class="value">{suite.total_tests}</div>
            </div>
            <div class="summary-card">
                <h3>Passed</h3>
                <div class="value">{suite.passed_tests}</div>
            </div>
            <div class="summary-card">
                <h3>Failed</h3>
                <div class="value failed">{suite.failed_tests}</div>
            </div>
            <div class="summary-card">
                <h3>Pass Rate</h3>
                <div class="value {'failed' if suite.pass_rate < 0.8 else 'warning' if suite.pass_rate < 0.9 else ''}">{suite.pass_rate:.1%}</div>
            </div>
            <div class="summary-card">
                <h3>Average Score</h3>
                <div class="value {'failed' if suite.average_score < 0.7 else 'warning' if suite.average_score < 0.8 else ''}">{suite.average_score:.2f}</div>
            </div>
            <div class="summary-card">
                <h3>Execution Time</h3>
                <div class="value">{suite.execution_time:.1f}s</div>
            </div>
        </div>
        
        <div class="category-stats">
            <h2>📊 Results by Category</h2>
            <div class="category-grid">
                {self._generate_category_stats_html(category_stats)}
            </div>
        </div>
        
        <div class="detailed-results">
            <h2>🔍 Detailed Test Results</h2>
            {self._generate_detailed_results_html(suite.results)}
        </div>
    </div>
    
    <script>
        // Toggle test details
        document.addEventListener('DOMContentLoaded', function() {{
            const testHeaders = document.querySelectorAll('.test-header');
            testHeaders.forEach(header => {{
                header.addEventListener('click', function() {{
                    const details = this.nextElementSibling;
                    details.classList.toggle('expanded');
                }});
            }});
            
            // Toggle collapsible sections
            const collapsibleHeaders = document.querySelectorAll('.collapsible-header');
            collapsibleHeaders.forEach(header => {{
                header.addEventListener('click', function() {{
                    const content = this.nextElementSibling;
                    content.classList.toggle('expanded');
                }});
            }});
        }});
    </script>
</body>
</html>
"""
        return html
    
    def _calculate_category_stats(self, results: List[EvalResult]) -> Dict[str, Dict[str, Any]]:
        """Calculate statistics by category"""
        category_stats = {}
        
        for result in results:
            # Extract category from test ID
            category = result.test_case_id.split('_')[0]
            category_name = self._get_category_name(category)
            
            if category_name not in category_stats:
                category_stats[category_name] = {
                    'total': 0,
                    'passed': 0,
                    'failed': 0,
                    'scores': []
                }
            
            category_stats[category_name]['total'] += 1
            category_stats[category_name]['scores'].append(result.score)
            
            if result.passed:
                category_stats[category_name]['passed'] += 1
            else:
                category_stats[category_name]['failed'] += 1
        
        # Calculate averages
        for category_name in category_stats:
            stats = category_stats[category_name]
            stats['pass_rate'] = stats['passed'] / stats['total'] if stats['total'] > 0 else 0
            stats['average_score'] = statistics.mean(stats['scores']) if stats['scores'] else 0
        
        return category_stats
    
    def _get_category_name(self, category_code: str) -> str:
        """Convert category code to readable name"""
        category_map = {
            'de': 'Data Extraction',
            'mpq': 'Meal Plan Quality',
            'sc': 'Safety Compliance',
            'ux': 'User Experience',
            'cf': 'Conversation Flow',
            'ec': 'Edge Cases',
            'perf': 'Performance'
        }
        return category_map.get(category_code, category_code)
    
    def _generate_category_stats_html(self, category_stats: Dict[str, Dict[str, Any]]) -> str:
        """Generate HTML for category statistics"""
        html_parts = []
        
        for category_name, stats in category_stats.items():
            pass_rate = stats['pass_rate']
            status_class = 'failed' if pass_rate < 0.8 else 'warning' if pass_rate < 0.9 else ''
            
            html_parts.append(f"""
                <div class="category-item {status_class}">
                    <div class="category-name">{category_name}</div>
                    <div class="category-metrics">
                        <span>{stats['passed']}/{stats['total']} passed</span>
                        <span>Rate: {pass_rate:.1%}</span>
                        <span>Score: {stats['average_score']:.2f}</span>
                    </div>
                </div>
            """)
        
        return ''.join(html_parts)
    
    def _generate_detailed_results_html(self, results: List[EvalResult]) -> str:
        """Generate HTML for detailed test results"""
        html_parts = []
        
        for result in results:
            status_class = 'passed' if result.passed else 'failed'
            status_text = 'PASSED' if result.passed else 'FAILED'
            
            # Generate details sections
            details_html = ""
            
            if result.errors:
                error_list = '<br>'.join(html.escape(error) for error in result.errors)
                details_html += f"""
                    <div class="error-list">
                        <strong>Errors:</strong><br>
                        {error_list}
                    </div>
                """
            
            if result.warnings:
                warning_list = '<br>'.join(html.escape(warning) for warning in result.warnings)
                details_html += f"""
                    <div class="warning-list">
                        <strong>Warnings:</strong><br>
                        {warning_list}
                    </div>
                """
            
            # Add collapsible sections for detailed data
            details_html += f"""
                <div class="collapsible-section">
                    <div class="collapsible-header">📋 Test Details</div>
                    <div class="collapsible-content">
                        <div class="json-display">{html.escape(json.dumps(result.details, indent=2, default=str))}</div>
                    </div>
                </div>
            """
            
            html_parts.append(f"""
                <div class="test-result {status_class}">
                    <div class="test-header">
                        <div class="test-info">
                            <div class="test-status {status_class}">{status_text}</div>
                            <div>
                                <strong>{result.test_case_id}</strong>
                                <div class="timestamp">{result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</div>
                            </div>
                        </div>
                        <div>
                            <div class="test-score {status_class}">{result.score:.2f}</div>
                            <div class="test-execution-time">{result.execution_time:.3f}s</div>
                        </div>
                    </div>
                    <div class="test-details">
                        {details_html}
                    </div>
                </div>
            """)
        
        return ''.join(html_parts)
    
    def generate_summary_report(self, suite: EvalSuite) -> str:
        """Generate a concise summary report"""
        category_stats = self._calculate_category_stats(suite.results)
        
        summary = f"""
AI Meal Plan Assistant - Evaluation Summary
==========================================

Overall Results:
- Total Tests: {suite.total_tests}
- Passed: {suite.passed_tests}
- Failed: {suite.failed_tests}
- Pass Rate: {suite.pass_rate:.1%}
- Average Score: {suite.average_score:.2f}
- Execution Time: {suite.execution_time:.1f}s

Category Breakdown:
"""
        
        for category_name, stats in category_stats.items():
            summary += f"""
{category_name}:
  - Tests: {stats['total']}, Passed: {stats['passed']}, Failed: {stats['failed']}
  - Pass Rate: {stats['pass_rate']:.1%}
  - Average Score: {stats['average_score']:.2f}
"""
        
        # Add failed tests details
        failed_tests = [r for r in suite.results if not r.passed]
        if failed_tests:
            summary += f"""
Failed Tests ({len(failed_tests)}):
"""
            for test in failed_tests:
                summary += f"  - {test.test_case_id}: Score {test.score:.2f}"
                if test.errors:
                    summary += f" (Errors: {', '.join(test.errors[:2])})"
                summary += "\n"
        
        return summary
