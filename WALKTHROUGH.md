# Complete DAST Project Walkthrough

## 🎯 Project Overview
This is an **AI-Powered Dynamic Application Security Testing (DAST)** pipeline that automatically scans web applications for vulnerabilities, classifies them using AI, and provides remediation guidance.

---

## 📋 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  GitHub Repository (DAST-security)                          │
│  └─ Vulnerable Node.js App (index.js)                       │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  Render.com (Hosting)                                       │
│  https://vulnerable-web-app-d0f8.onrender.com              │
│  └─ Live vulnerable application running 24/7                │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  GitHub Actions Workflow (Auto-triggered)                   │
│  └─ Runs on: Push, PR, Schedule (Monday 2 AM)              │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  OWASP ZAP Scanner                                          │
│  └─ Scans live app for vulnerabilities                      │
│  └─ Generates report.json                                   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  AI Classification (Google Gemini)                          │
│  └─ Analyzes vulnerabilities                                │
│  └─ Provides severity scores & remediation                  │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  Slack Reporter                                             │
│  └─ Sends alerts to #security-alerts channel                │
└─────────────────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  Build Breaker                                              │
│  └─ Fails CI/CD if critical vulnerabilities found           │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Component Breakdown

### 1. **Vulnerable Web Application** (`index.js`)
A purposely insecure Node.js/Express app with these vulnerabilities:

```javascript
// ❌ Reflected XSS Vulnerability
app.get('/search', (req, res) => {
  const q = req.query.q || '';
  res.send(`<h1>Results for: ${q}</h1>`);  // No sanitization!
});

// ❌ Open Redirect Vulnerability
app.get('/redirect', (req, res) => {
  const url = req.query.url;
  res.redirect(url);  // Accepts any URL!
});

// ❌ Insecure Authentication
app.post('/login', (req, res) => {
  const { username, password } = req.body;
  // Plain text passwords, verbose error messages
  const user = users.find(u => u.username === username && u.password === password);
});

// ❌ SQL Injection (Simulated)
app.get('/user', (req, res) => {
  const id = req.query.id;
  res.send(`Fetched user with ID: ${id}`);  // No parameterization
});

// ❌ Sensitive Data Exposure
app.get('/config', (req, res) => {
  res.send({
    dbPassword: 'supersecret123',
    apiKey: 'sk-proj-abcd1234'  // Exposed credentials!
  });
});
```

**Live URL**: https://vulnerable-web-app-d0f8.onrender.com

---

### 2. **OWASP ZAP Scanner** (GitHub Actions)

The workflow file `.github/workflows/zap-baseline.yml` triggers automatic scans:

```yaml
# Triggers
on:
  push:                    # Every code push
  pull_request:            # Every PR
  schedule:                # Weekly scans
    - cron: "0 2 * * 1"    # Mondays at 2 AM
```

**What ZAP Does**:
- 🕷️ Crawls the entire application
- 🔍 Tests for 100+ vulnerability types
- 📊 Generates JSON/HTML reports
- ⚡ Active scanning with payloads

**Example ZAP Findings**:
```json
{
  "alert": "Cross Site Scripting (Reflected)",
  "risk": "High",
  "url": "https://vulnerable-web-app-d0f8.onrender.com/search?q=<script>alert(1)</script>",
  "evidence": "<script>alert(1)</script>",
  "solution": "Validate all input and encode output"
}
```

---

### 3. **AI Classification Engine** (`ai_classifier_v2.py`)

Uses **Google Gemini** to analyze vulnerabilities:

```python
def classify_vulnerability(vuln_data):
    """
    Sends vulnerability to Gemini AI for:
    - Severity scoring (1-10)
    - Exploitability analysis
    - Business impact assessment
    - Specific remediation steps
    """
    prompt = f"""
    Analyze this security vulnerability:
    
    Type: {vuln_data['alert']}
    URL: {vuln_data['url']}
    Evidence: {vuln_data['evidence']}
    
    Provide:
    1. Severity score (1-10)
    2. Exploitability rating
    3. Business impact
    4. Step-by-step remediation
    """
    
    response = gemini.generate_content(prompt)
    return parse_ai_response(response)
```

**AI Output Example**:
```
🤖 AI Analysis:
Severity: 9.5/10 (Critical)
Exploitability: HIGH - Can be exploited in <5 minutes
Business Impact: Account takeover, data theft, malware injection
Remediation:
  1. Implement Content Security Policy (CSP)
  2. Use DOMPurify or similar sanitization library
  3. Encode all user input: escape HTML entities
  4. Add X-XSS-Protection header
```

---

### 4. **Slack Reporter** (`slack_reporter_full.py`)

Sends rich notifications to your Slack workspace:

```python
# Formats findings into Slack blocks
message = {
    "channel": "#security-alerts",
    "blocks": [
        {
            "type": "header",
            "text": "🚨 Security Scan Complete"
        },
        {
            "type": "section",
            "text": f"Found {critical_count} CRITICAL vulnerabilities"
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Alert:* {vuln['alert']}"},
                {"type": "mrkdwn", "text": f"*Severity:* {ai_severity}/10"},
                {"type": "mrkdwn", "text": f"*URL:* {vuln['url']}"},
                {"type": "mrkdwn", "text": f"*Fix:* {remediation}"}
            ]
        }
    ]
}
```

**Slack Notification Example**:
```
🚨 Security Scan Complete
━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Summary:
  🔴 Critical: 3
  🟠 High: 5
  🟡 Medium: 12

━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 CRITICAL: Cross Site Scripting
URL: /search?q=test
AI Severity: 9.5/10
Remediation: Sanitize all user input...

[View Full Report] [Download JSON]
```

---

### 5. **Build Breaker** (`build_breaker.py`)

Enforces security gates in CI/CD:

```python
# Configuration
MAX_CRITICAL_VULNS = 0     # Zero tolerance
MAX_HIGH_VULNS = 3         # Max 3 high severity
MAX_MEDIUM_VULNS = 10      # Max 10 medium severity
AI_SEVERITY_THRESHOLD = 8.0 # AI score limit

# Decision Logic
if critical_count > MAX_CRITICAL_VULNS:
    print("❌ BUILD FAILED: Critical vulnerabilities detected")
    sys.exit(1)  # Fail the pipeline
elif high_count > MAX_HIGH_VULNS:
    print("⚠️ BUILD WARNING: Too many high severity issues")
    sys.exit(1)
else:
    print("✅ BUILD PASSED: Security checks passed")
    sys.exit(0)
```

---

## 🎬 Complete Workflow Example

### **Scenario**: Developer pushes vulnerable code

```bash
# Developer commits new feature
git add vulnerable-feature.js
git commit -m "Add user search feature"
git push origin main
```

### **Step-by-Step Execution**:

**[00:00] GitHub Actions Triggered**
```
✓ Detected push to main branch
✓ Starting workflow: ZAP Baseline (DAST)
✓ Runner: ubuntu-latest
```

**[00:15] Setup Phase**
```
✓ Checkout code
✓ Setup Python 3.9
✓ Install dependencies (ZAP, Gemini SDK, Slack SDK)
```

**[00:30] Target Validation**
```
✓ Checking https://vulnerable-web-app-d0f8.onrender.com/health
✓ App is responding (200 OK)
✓ Starting ZAP scan...
```

**[01:00] ZAP Scanning**
```
🕷️ Crawling application...
   └─ Found 8 endpoints
   └─ /search, /redirect, /login, /user, /config, /health, /admin, /api

🔍 Active scanning...
   └─ Testing XSS payloads
   └─ Testing SQL injection
   └─ Testing authentication flaws
   └─ Testing sensitive data exposure

📊 Scan complete:
   └─ 142 tests performed
   └─ 18 vulnerabilities found
```

**[01:30] AI Classification**
```
🤖 Analyzing with Google Gemini...

Vulnerability 1/18:
  Type: Reflected XSS
  Original Risk: High
  AI Severity: 9.5/10
  Exploitability: HIGH
  Impact: Account takeover, data theft
  Remediation: Implement input sanitization...

Vulnerability 2/18:
  Type: Open Redirect
  Original Risk: Medium
  AI Severity: 7.2/10
  Exploitability: MEDIUM
  Impact: Phishing attacks
  Remediation: Validate redirect URLs...

[Processing 16 more...]
```

**[02:00] Slack Notification**
```
✓ Formatting report for Slack
✓ Sending to #security-alerts
✓ Message delivered successfully
```

**[02:10] Build Breaker Evaluation**
```
🔍 Checking security thresholds:

Critical vulnerabilities: 3
Maximum allowed: 0
❌ THRESHOLD EXCEEDED!

High vulnerabilities: 5
Maximum allowed: 3
❌ THRESHOLD EXCEEDED!

━━━━━━━━━━━━━━━━━━━━━━━━━
❌ BUILD FAILED
Reason: 3 critical vulnerabilities detected
Action: Fix vulnerabilities before merging
━━━━━━━━━━━━━━━━━━━━━━━━━
```

**[02:15] Reports Generated**
```
✓ report.html → GitHub Artifacts
✓ report.json → GitHub Artifacts
✓ Slack notification → Sent
✓ Build status → FAILED
```

---

## 🔍 Viewing Results

### **Option 1: GitHub Actions**
1. Go to: `github.com/Daksh-khandelwal-1495/DAST-security`
2. Click **Actions** tab
3. Select latest workflow run
4. Download artifacts: `zap-reports`

### **Option 2: Slack**
- Check `#security-alerts` channel
- Review AI-analyzed vulnerabilities
- Click links to view full details

### **Option 3: Local Testing**
```bash
# Run ZAP scan locally
docker run -t ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py \
  -t https://vulnerable-web-app-d0f8.onrender.com \
  -r report.html

# Analyze with AI
python ai_classifier_v2.py report.json

# Send to Slack
python slack_reporter_full.py report.json javascript
```

---

## 🛠️ Testing the Vulnerabilities

### **Test XSS**:
```bash
curl "https://vulnerable-web-app-d0f8.onrender.com/search?q=<script>alert('XSS')</script>"
# Response will include unescaped script tag
```

### **Test Open Redirect**:
```bash
curl -L "https://vulnerable-web-app-d0f8.onrender.com/redirect?url=https://evil.com"
# Will redirect to evil.com without validation
```

### **Test Credential Exposure**:
```bash
curl "https://vulnerable-web-app-d0f8.onrender.com/config"
# Returns:
# {
#   "dbPassword": "supersecret123",
#   "apiKey": "sk-proj-abcd1234"
# }
```

---

## 📊 Key Metrics

| Metric | Value |
|--------|-------|
| **Scan Frequency** | Every push + Weekly |
| **Average Scan Time** | 2-3 minutes |
| **Vulnerabilities Tested** | 100+ types |
| **AI Classification Time** | ~5 seconds per vuln |
| **Slack Delivery** | Real-time |
| **Build Break Threshold** | 0 Critical, 3 High |

---

## 🎓 What You've Built

✅ **Automated DAST Pipeline** - No manual intervention needed
✅ **AI-Enhanced Analysis** - Smarter than traditional scanners
✅ **Real-time Alerting** - Instant Slack notifications
✅ **CI/CD Integration** - Blocks vulnerable code
✅ **Compliance Ready** - Audit trail via GitHub Actions
✅ **Scalable** - Works with any web application
✅ **Cost Effective** - Free tier compatible

---

## 🚀 Next Steps

1. **Configure Slack** (if not done):
   - Add `SLACK_BOT_TOKEN` to GitHub Secrets
   - Set `SLACK_CHANNEL` variable

2. **Add Gemini API** (if not done):
   - Get free API key from Google AI Studio
   - Add `GEMINI_API_KEY` to GitHub Secrets

3. **Customize Thresholds**:
   - Edit build breaker limits in workflow
   - Adjust AI severity thresholds

4. **Expand Coverage**:
   - Add more endpoints to test
   - Configure ZAP custom scan policies
   - Add authentication for protected routes

---

## 📚 Project Files Reference

- `index.js` - Vulnerable web application
- `Dockerfile` - Container configuration
- `render.yaml` - Render deployment config
- `.github/workflows/zap-baseline.yml` - CI/CD pipeline
- `ai_classifier_v2.py` - AI analysis engine
- `slack_reporter_full.py` - Slack integration
- `build_breaker.py` - Security gate enforcement
- `requirements.txt` - Python dependencies

---

**Status**: ✅ Fully Operational
**Live URL**: https://vulnerable-web-app-d0f8.onrender.com
**Repository**: github.com/Daksh-khandelwal-1495/DAST-security
