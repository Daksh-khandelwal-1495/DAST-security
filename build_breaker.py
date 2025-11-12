#!/usr/bin/env python3
"""
Build Breaker - Fails CI/CD pipeline for critical vulnerabilities
Integrates with DAST scan results to enforce security gates
"""

import os
import json
import sys
from typing import Dict, List, Tuple
from dotenv import load_dotenv

load_dotenv()


class BuildBreaker:
    """
    Analyzes security scan results and decides whether to break the build
    based on configurable severity thresholds
    """
    
    def __init__(self):
        """Initialize with configuration from environment variables"""
        # Thresholds - fail build if exceeded
        self.max_critical = int(os.getenv('MAX_CRITICAL_VULNS', '0'))
        self.max_high = int(os.getenv('MAX_HIGH_VULNS', '3'))
        self.max_medium = int(os.getenv('MAX_MEDIUM_VULNS', '10'))
        
        # AI severity threshold (0-10 scale)
        self.ai_severity_threshold = float(os.getenv('AI_SEVERITY_THRESHOLD', '8.0'))
        
        # Build breaking mode
        self.break_build = os.getenv('BREAK_BUILD_ON_CRITICAL', 'true').lower() == 'true'
        
        print(f"🔒 Build Breaker Configuration:")
        print(f"   Max Critical: {self.max_critical}")
        print(f"   Max High: {self.max_high}")
        print(f"   Max Medium: {self.max_medium}")
        print(f"   AI Severity Threshold: {self.ai_severity_threshold}")
        print(f"   Break Build: {'✅ Enabled' if self.break_build else '❌ Disabled (Report Only)'}")
    
    def parse_zap_report(self, report_path: str) -> Dict:
        """Parse ZAP JSON report and extract vulnerability counts"""
        print(f"\n📖 Reading ZAP report: {report_path}")
        
        with open(report_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        site = data.get('site', [{}])[0]
        alerts = site.get('alerts', [])
        
        # Count by severity
        counts = {
            'Critical': 0,
            'High': 0,
            'Medium': 0,
            'Low': 0,
            'Informational': 0
        }
        
        high_severity_vulns = []
        
        for alert in alerts:
            risk = alert.get('riskdesc', 'Low').split()[0]
            counts[risk] = counts.get(risk, 0) + 1
            
            # Track critical/high severity for detailed reporting
            if risk in ['Critical', 'High']:
                high_severity_vulns.append({
                    'name': alert.get('name'),
                    'risk': risk,
                    'ai_severity': alert.get('ai_severity_score', 0),
                    'ai_category': alert.get('ai_category', 'UNKNOWN'),
                    'instances': len(alert.get('instances', []))
                })
        
        return {
            'counts': counts,
            'total': len(alerts),
            'high_severity_vulns': high_severity_vulns,
            'site': site.get('@name', 'Unknown')
        }
    
    def check_thresholds(self, report_data: Dict) -> Tuple[bool, List[str]]:
        """
        Check if vulnerability counts exceed thresholds
        
        Returns:
            Tuple of (should_break_build, list_of_violations)
        """
        counts = report_data['counts']
        violations = []
        
        print(f"\n🔍 Checking Security Thresholds:")
        print(f"   Found: Critical={counts.get('Critical', 0)}, High={counts.get('High', 0)}, Medium={counts.get('Medium', 0)}")
        
        # Check critical vulnerabilities
        if counts.get('Critical', 0) > self.max_critical:
            msg = f"❌ CRITICAL: Found {counts['Critical']} critical vulnerabilities (max allowed: {self.max_critical})"
            violations.append(msg)
            print(f"   {msg}")
        
        # Check high vulnerabilities
        if counts.get('High', 0) > self.max_high:
            msg = f"⚠️  HIGH: Found {counts['High']} high vulnerabilities (max allowed: {self.max_high})"
            violations.append(msg)
            print(f"   {msg}")
        
        # Check medium vulnerabilities
        if counts.get('Medium', 0) > self.max_medium:
            msg = f"⚡ MEDIUM: Found {counts['Medium']} medium vulnerabilities (max allowed: {self.max_medium})"
            violations.append(msg)
            print(f"   {msg}")
        
        # Check AI severity scores
        high_ai_severity = [
            v for v in report_data['high_severity_vulns']
            if v['ai_severity'] >= self.ai_severity_threshold
        ]
        
        if high_ai_severity:
            msg = f"🤖 AI ALERT: {len(high_ai_severity)} vulnerabilities with AI severity >= {self.ai_severity_threshold}"
            violations.append(msg)
            print(f"   {msg}")
        
        should_break = len(violations) > 0
        
        if not should_break:
            print(f"   ✅ All thresholds passed!")
        
        return should_break, violations
    
    def generate_failure_report(self, report_data: Dict, violations: List[str]) -> str:
        """Generate detailed failure report"""
        
        report = []
        report.append("=" * 70)
        report.append("🚨 BUILD FAILED - SECURITY GATE VIOLATION")
        report.append("=" * 70)
        report.append("")
        report.append(f"Target: {report_data['site']}")
        report.append(f"Total Vulnerabilities: {report_data['total']}")
        report.append("")
        report.append("VIOLATIONS:")
        for violation in violations:
            report.append(f"  {violation}")
        report.append("")
        
        # List critical and high severity vulnerabilities
        if report_data['high_severity_vulns']:
            report.append("CRITICAL/HIGH SEVERITY ISSUES:")
            report.append("")
            for i, vuln in enumerate(report_data['high_severity_vulns'][:10], 1):
                report.append(f"  {i}. {vuln['risk']}: {vuln['name']}")
                report.append(f"     Category: {vuln['ai_category']}")
                report.append(f"     AI Severity: {vuln['ai_severity']}/10")
                report.append(f"     Instances: {vuln['instances']}")
                report.append("")
        
        report.append("=" * 70)
        report.append("REQUIRED ACTIONS:")
        report.append("  1. Review the vulnerabilities listed above")
        report.append("  2. Implement fixes using the remediation guidance in Slack")
        report.append("  3. Re-run the security scan")
        report.append("  4. Build will pass once vulnerabilities are below thresholds")
        report.append("=" * 70)
        report.append("")
        report.append("💡 TIP: Check Slack for AI-powered remediation guidance!")
        report.append("")
        
        return "\n".join(report)
    
    def generate_success_report(self, report_data: Dict) -> str:
        """Generate success report"""
        
        counts = report_data['counts']
        
        report = []
        report.append("=" * 70)
        report.append("✅ BUILD PASSED - SECURITY GATE")
        report.append("=" * 70)
        report.append("")
        report.append(f"Target: {report_data['site']}")
        report.append(f"Total Vulnerabilities: {report_data['total']}")
        report.append("")
        report.append("SEVERITY BREAKDOWN:")
        report.append(f"  🔴 Critical: {counts.get('Critical', 0)} (max: {self.max_critical})")
        report.append(f"  🟠 High: {counts.get('High', 0)} (max: {self.max_high})")
        report.append(f"  🟡 Medium: {counts.get('Medium', 0)} (max: {self.max_medium})")
        report.append(f"  🟢 Low: {counts.get('Low', 0)}")
        report.append(f"  ℹ️  Info: {counts.get('Informational', 0)}")
        report.append("")
        report.append("All security thresholds met! ✨")
        report.append("=" * 70)
        
        return "\n".join(report)
    
    def evaluate(self, report_path: str) -> int:
        """
        Main evaluation method
        
        Returns:
            Exit code: 0 for success, 1 for failure
        """
        print("\n" + "=" * 70)
        print("🔒 Security Gate Evaluation")
        print("=" * 70)
        
        # Parse report
        report_data = self.parse_zap_report(report_path)
        
        # Check thresholds
        should_break, violations = self.check_thresholds(report_data)
        
        # Generate report
        if should_break and self.break_build:
            print("\n" + self.generate_failure_report(report_data, violations))
            return 1  # Fail the build
        elif should_break and not self.break_build:
            print(f"\n⚠️  VIOLATIONS FOUND (Report-Only Mode):")
            for violation in violations:
                print(f"   {violation}")
            print(f"\n✅ Build continues (BREAK_BUILD_ON_CRITICAL=false)")
            print("\n" + self.generate_success_report(report_data))
            return 0  # Pass the build (report only)
        else:
            print("\n" + self.generate_success_report(report_data))
            return 0  # Pass the build


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python build_breaker.py <zap-report.json>")
        sys.exit(1)
    
    report_path = sys.argv[1]
    
    if not os.path.exists(report_path):
        print(f"❌ Report file not found: {report_path}")
        sys.exit(1)
    
    breaker = BuildBreaker()
    exit_code = breaker.evaluate(report_path)
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
