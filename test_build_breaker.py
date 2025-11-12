#!/usr/bin/env python3
"""
Test Build Breaker functionality with different scenarios
"""

import json
import os
from build_breaker import BuildBreaker


def create_test_report(critical=0, high=0, medium=0, low=0):
    """Create a test ZAP report with specified vulnerability counts"""
    
    alerts = []
    
    # Add critical vulnerabilities
    for i in range(critical):
        alerts.append({
            "name": f"Critical Vulnerability {i+1}",
            "riskdesc": "Critical (High)",
            "desc": "Critical security issue found",
            "ai_severity_score": 9.5,
            "ai_category": "CRITICAL",
            "instances": [{"uri": f"https://example.com/critical{i}"}]
        })
    
    # Add high vulnerabilities
    for i in range(high):
        alerts.append({
            "name": f"High Severity Issue {i+1}",
            "riskdesc": "High (Medium)",
            "desc": "High severity security issue",
            "ai_severity_score": 8.5,
            "ai_category": "HIGH",
            "instances": [{"uri": f"https://example.com/high{i}"}]
        })
    
    # Add medium vulnerabilities
    for i in range(medium):
        alerts.append({
            "name": f"Medium Severity Issue {i+1}",
            "riskdesc": "Medium (Medium)",
            "desc": "Medium severity security issue",
            "ai_severity_score": 6.0,
            "ai_category": "MEDIUM",
            "instances": [{"uri": f"https://example.com/medium{i}"}]
        })
    
    # Add low vulnerabilities
    for i in range(low):
        alerts.append({
            "name": f"Low Severity Issue {i+1}",
            "riskdesc": "Low (Low)",
            "desc": "Low severity security issue",
            "ai_severity_score": 3.0,
            "ai_category": "LOW",
            "instances": [{"uri": f"https://example.com/low{i}"}]
        })
    
    report = {
        "site": [{
            "@name": "https://test-application.com",
            "alerts": alerts
        }]
    }
    
    return report


def test_scenario(name, critical, high, medium, low, expected_result):
    """Test a specific scenario"""
    print("\n" + "=" * 70)
    print(f"🧪 TEST: {name}")
    print("=" * 70)
    
    # Create test report
    report = create_test_report(critical, high, medium, low)
    report_path = f"test_report_{name.replace(' ', '_').lower()}.json"
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"   Created test report: Critical={critical}, High={high}, Medium={medium}, Low={low}")
    
    # Test with build breaker
    breaker = BuildBreaker()
    exit_code = breaker.evaluate(report_path)
    
    # Verify result
    if expected_result == "PASS" and exit_code == 0:
        print(f"\n   ✅ TEST PASSED: Build passed as expected")
        result = "✅ PASS"
    elif expected_result == "FAIL" and exit_code == 1:
        print(f"\n   ✅ TEST PASSED: Build failed as expected")
        result = "✅ PASS"
    else:
        print(f"\n   ❌ TEST FAILED: Expected {expected_result}, got {'FAIL' if exit_code == 1 else 'PASS'}")
        result = "❌ FAIL"
    
    # Cleanup
    if os.path.exists(report_path):
        os.remove(report_path)
    
    return result


def main():
    """Run all test scenarios"""
    print("\n🚀 Build Breaker Test Suite")
    print("=" * 70)
    
    # Store results
    results = []
    
    # Test Scenario 1: Clean build - should PASS
    result = test_scenario(
        "Clean Build",
        critical=0, high=0, medium=0, low=5,
        expected_result="PASS"
    )
    results.append(("Clean Build", result))
    
    # Test Scenario 2: Within thresholds - should PASS
    result = test_scenario(
        "Within Thresholds",
        critical=0, high=2, medium=8, low=5,
        expected_result="PASS"
    )
    results.append(("Within Thresholds", result))
    
    # Test Scenario 3: One critical - should FAIL
    result = test_scenario(
        "One Critical Issue",
        critical=1, high=0, medium=0, low=0,
        expected_result="FAIL"
    )
    results.append(("One Critical Issue", result))
    
    # Test Scenario 4: Too many high - should FAIL
    result = test_scenario(
        "Too Many High",
        critical=0, high=5, medium=0, low=0,
        expected_result="FAIL"
    )
    results.append(("Too Many High", result))
    
    # Test Scenario 5: Too many medium - should FAIL
    result = test_scenario(
        "Too Many Medium",
        critical=0, high=0, medium=15, low=0,
        expected_result="FAIL"
    )
    results.append(("Too Many Medium", result))
    
    # Test Scenario 6: Edge case (exactly at threshold) - should PASS
    result = test_scenario(
        "Exactly At Threshold",
        critical=0, high=3, medium=10, low=0,
        expected_result="PASS"
    )
    results.append(("Exactly At Threshold", result))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, r in results if r == "✅ PASS")
    failed = sum(1 for _, r in results if r == "❌ FAIL")
    
    for name, result in results:
        print(f"   {result} {name}")
    
    print(f"\n   Total: {len(results)} | Passed: {passed} | Failed: {failed}")
    
    if failed == 0:
        print("\n   ✨ All tests passed!")
    else:
        print(f"\n   ⚠️  {failed} test(s) failed")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
